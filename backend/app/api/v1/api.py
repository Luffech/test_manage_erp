# backend/app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import sistemas
from .endpoints import modulo
from .endpoints import sap_automacao
from .endpoints import auth
from .endpoints import usuario 
from .endpoints import admin_data 
from .endpoints import caso_teste # <-- NOVO
from .endpoints import tester # <-- NOVO
from .endpoints import metrica # <-- NOVO

# Cria o roteador principal da API v1
api_router = APIRouter()

# Rotas de Autenticação e Seed (Dev)
api_router.include_router(auth.router, tags=["Autenticação"])
api_router.include_router(admin_data.router, tags=["DEV_TOOLS"]) 

# Rotas de CRUD
api_router.include_router(sistemas.router, prefix="/sistemas", tags=["Sistemas"])
api_router.include_router(modulo.router, prefix="/modulos", tags=["Módulos"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"]) 
api_router.include_router(caso_teste.router, prefix="/casos_teste", tags=["Casos de Teste"]) # <-- NOVO
api_router.include_router(tester.router, prefix="/tester", tags=["Testador"]) # <-- NOVO
api_router.include_router(metrica.router, prefix="/metrics", tags=["Métricas"]) # <-- NOVO

# Rota SAP
api_router.include_router(sap_automacao.router, prefix="/sap", tags=["SAP"])