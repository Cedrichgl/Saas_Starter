from fastapi import APIRouter, Depends

from app.dependancies.roles import require_role
from app.models.user import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def admin_dashboard(current_user=Depends(require_role(UserRole.ADMIN))):
    return {"Message": "Bienvenue Admin"}
