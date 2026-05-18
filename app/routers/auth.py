import token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependancies.auth import get_current_user
from app.models.user import User
from app.schemas.token import Token, TokenData
from app.schemas.user import UserBase, UserCreate, UserResponse, UserRole, UserUpdate
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


# register
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    utilisateur_existant = db.query(User.email == user.email).first()
    if utilisateur_existant:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déja")
    nouvel_utilisateur = User(
        email=user.email, hashed_password=hash_password(user.password)
    )
    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)
    return nouvel_utilisateur


# login
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
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
