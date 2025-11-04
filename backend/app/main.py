# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

# Cria a aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    # Permitindo todas as origens (em desenvolvimento)
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o roteador principal da v1, prefixando todas as suas rotas com /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", summary="Endpoint raiz da API")
def read_root():
    return {"message": "Test Manager ERP Backend iniciado!"}

@app.get("/health", summary="Verifica a saúde da API")
def health_check():
    return {"status": "healthy"}