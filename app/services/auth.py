from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# mot de passe
def hash_password(password: str) -> str:
    # cette fonction va hasher le mdp
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # compare le mot de passe de passe hashé avec le mot de passe stocké en base
    return pwd_context.verify(plain_password, hashed_password)


# JWT
def create_access_token(data: dict) -> str:
    """Génère un JWT à partir de données (ex: l'email)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> str:
    """Vérifie un JWT et retourne l'email s'il est valide"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise ValueError("Token invalide")
        return email
    except JWTError:
        raise ValueError("Token invalide ou expiré")
