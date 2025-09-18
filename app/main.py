from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

from app.routers.academico import router
from app.database import Base, engine

app = FastAPI(title="Consumer Service")

Base.metadata.create_all(bind=engine)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

AUTH_MS_URL = os.getenv("AUTH_MS_URL", "http://127.0.0.1:8001")

def validate_with_auth_ms(token: str):
    r = requests.post(f"{AUTH_MS_URL}/api/v1/authentication/", json={"token": token}, timeout=5)
    if r.status_code != 200:
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = r.text
        raise HTTPException(status_code=400, detail=f"Token inválido: {detail}")
    return r.json()

@app.get("/api/v1/home/")
def home(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # já sem o prefixo "Bearer "
    data = validate_with_auth_ms(token)
    return {"message": "Acesso autorizado", "user": {"username": data.get("username"), "nome": data.get("nome")}}
