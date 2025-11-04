# backend/app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import sistemas
from .endpoints import modulo
from .endpoints import sap_automacao
from .endpoints import auth # << NOVO

# Cria o roteador principal da API v1
api_router = APIRouter()

# Inclui o roteador de autenticação (sem prefixo, para ter a rota /api/v1/login)
api_router.include_router(auth.router, tags=["Autenticação"])

# Inclui os roteadores de CRUD
api_router.include_router(sistemas.router, prefix="/sistemas", tags=["Sistemas"])
api_router.include_router(modulo.router, prefix="/modulos", tags=["Módulos"])

# Inclui a rota SAP
api_router.include_router(sap_automacao.router, prefix="/sap", tags=["SAP"])