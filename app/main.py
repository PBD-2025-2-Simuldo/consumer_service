from fastapi import FastAPI, Header, HTTPException, Request
import requests
import os

app = FastAPI(title="Consumer Service")

# URL do microserviço de autenticação
AUTH_MS_URL = os.getenv("AUTH_MS_URL", "http://127.0.0.1:8001")

@app.get("/api/v1/home/")
def home(authorization: str | None = Header(None)):
    # Espera header Authorization: Bearer <token>
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    # extrai token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    token = parts[1]

    # chama o MS para validar o token
    try:
        r = requests.post(f"{AUTH_MS_URL}/api/v1/authentication/", json={"token": token}, timeout=5)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao conectar no Auth MS: {str(e)}")

    if r.status_code != 200:
        # retorna 400 com mensagem de erro
        detail = r.json().get("detail") if r.headers.get("content-type","").startswith("application/json") else r.text
        raise HTTPException(status_code=400, detail=f"Token inválido: {detail}")

    data = r.json()
    return {"message": "Acesso autorizado", "user": {"username": data.get("username"), "nome": data.get("nome")}}
