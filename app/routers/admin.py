from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.database import get_db
from app.dependancies.auth import get_current_user
from app.dependancies.roles import require_role
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserRoleUpdate, UserUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def admin_dashboard(current_user=Depends(require_role(UserRole.ADMIN))):
    return {"Message": "Bienvenue Admin"}


# liste tous les utilisateurs
@router.get("/users", response_model=list[UserResponse])
async def get_users(
    db: Session = Depends(get_db), current_user=Depends(require_role(UserRole.ADMIN))
):
    user = db.query(User).filter().all()
    return user


# get un user
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="L'utisateur est introuvable")
    return user


# put user
@router.put("/users/{user_id}/role", response_model=UserResponse)
async def put_user(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=("L'utilisateur est introuvable"))
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user


# delete user
@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")
    db.delete(db_user)
    db.commit()
    return db_user
