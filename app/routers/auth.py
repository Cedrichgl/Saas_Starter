import token
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependancies.auth import get_current_user
from app.limiter import limiter
from app.main import limiter
from app.models.user import User
from app.schemas.token import Token, TokenData
from app.schemas.user import UserBase, UserCreate, UserResponse, UserRole, UserUpdate
from app.services.auth import create_access_token, hash_password, verify_password
from app.services.email import send_reset_email, send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


# register
@router.post("/register", response_model=UserResponse, status_code=201)
@limiter.limit("5/minutes")
async def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    utilisateur_existant = db.query(User.email == user.email).first()
    if utilisateur_existant:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déjà")
    nouvel_utilisateur = User(
        email=user.email, hashed_password=hash_password(user.password)
    )
    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)
    token = create_access_token(data={"sub": user.email})
    await send_verification_email(user.email, token)
    return nouvel_utilisateur


# login
@router.post("/login", response_model=Token)
@limiter.limit("3/minutes")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token, token_type="bearer")


# getme
@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


# verify emaikl
@router.get("/verify-email", response_model=dict)
async def verify_email(token: str = Query(), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token invalide"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token invalide ou expiré"
        )
    # Recherche utilisateur
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable"
        )

    # Vérification email
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return {"Message": "Email vérifié avec Succès"}

    # Forgot password
    @router.post("/forgot_password")
    async def forgot_password(email: str, bd: Session = Depends(get_db)):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=400, detail="Cette adresse e-mail n'existe pas"
            )
            # Création token reset
        token = create_access_token(data={"sub": user.email})

        # payload = {"sub": str(user.id), "exp": expire, "type": "reset_password"}
        # reset_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        reset_link = f"http://localhost:8000/reset-password?token={token}"

        await send_reset_email(user.email, reset_link)

        return {"message": "Lien de réinitialisation envoyé"}
