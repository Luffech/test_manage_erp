# backend/app/api/v1/endpoints/usuario.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import UsuarioService
from app.api.v1.deps import require_admin # Importa o Guard de Admin
from .sistemas import get_db_session 

router = APIRouter()

# Dependência para obter o serviço de Usuário
def get_usuario_service(db: AsyncSession = Depends(get_db_session)) -> UsuarioService:
    return UsuarioService(db)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, 
             summary="Criar um novo usuário (Admin)",
             dependencies=[Depends(require_admin)]) # <-- Protegido por Admin
async def create_user(
    user: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service)
):
    """ Cria um novo usuário na base de dados. """
    return await service.create_user(user)

@router.get("/", response_model=Sequence[UsuarioResponse], 
            summary="Listar todos os usuários (Admin)",
            dependencies=[Depends(require_admin)]) # <-- Protegido por Admin
async def get_users(
    service: UsuarioService = Depends(get_usuario_service)
):
    """ Retorna uma lista de todos os usuários. """
    return await service.get_all_users()

@router.put("/{email}", response_model=UsuarioResponse, 
            summary="Atualizar um usuário por email (Admin)",
            dependencies=[Depends(require_admin)]) # <-- Protegido por Admin
async def update_user(
    email: str,
    user_data: UsuarioUpdate,
    service: UsuarioService = Depends(get_usuario_service)
):
    """ Atualiza as informações de um usuário existente. """
    updated_user = await service.update_user(email, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT, 
               summary="Apagar um usuário por email (Admin)",
               dependencies=[Depends(require_admin)]) # <-- Protegido por Admin
async def delete_user(
    email: str,
    service: UsuarioService = Depends(get_usuario_service)
):
    """ Apaga um usuário da base de dados. """
    success = await service.delete_user(email)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return