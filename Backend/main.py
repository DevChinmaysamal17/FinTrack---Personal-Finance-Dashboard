from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from Backend.database import engine
from Backend import models
from Backend.routers import auth, users, transactions, categories, budgets
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from Backend.database import engine
from Backend import models, oauth2
from Backend.hashing import Hash
from Backend.dependencies import get_db
from Backend.schemas import (
    UserResponse,
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(budgets.router)

# CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="Frontend"), name="static")

@app.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(oauth2.get_current_user)):
    return current_user


# Serve Frontend
@app.get("/")
def serve_frontend():
    return FileResponse("Frontend/login.html")




