from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import Base, engine
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.routers import admin, auth

app = FastAPI()

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)


app.include_router(auth.router)
app.include_router(admin.router)


# initier le limit
limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")

# Attacher le limiter à l'app
app.state.limiter = limiter


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
