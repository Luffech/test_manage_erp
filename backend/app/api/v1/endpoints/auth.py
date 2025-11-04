# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Token, LoginInput
from app.services.auth_service import AuthService
from .sistemas import get_db_session # Reutiliza a dependência da sessão

router = APIRouter()

def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(db)

@router.post("/login", response_model=Token, summary="Autenticação e geração de JWT")
async def login(
    credentials: LoginInput,
    service: AuthService = Depends(get_auth_service)
):
    # O username será interpretado como email
    user = await service.authenticate_user(credentials)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou usuário inativo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token JWT para o cliente
    return service.generate_token(user)