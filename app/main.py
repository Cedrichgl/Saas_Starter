from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
