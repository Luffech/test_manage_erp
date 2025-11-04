# backend/app/services/usuario_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.models import Usuario, NivelAcesso
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas import UsuarioCreate, UsuarioUpdate

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.repo = UsuarioRepository(db)
        self.db = db # Mantém o db para consultas de validação

    async def create_user(self, user_data: UsuarioCreate) -> Usuario:
        """ Cria um usuário, incluindo validação de unicidade de email e nível de acesso. """
        # 1. Verifica se o email já existe
        existing_user = await self.repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já registrado."
            )
        
        # 2. Validação do nivel_acesso_id
        nivel_acesso_result = await self.db.execute(
            select(NivelAcesso).where(NivelAcesso.id == user_data.nivel_acesso_id)
        )
        if not nivel_acesso_result.scalars().first():
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nível de acesso inválido."
            )

        return await self.repo.create_user(user_data)

    async def get_all_users(self) -> Sequence[Usuario]:
        return await self.repo.get_all_users()

    async def update_user(self, current_email: str, user_data: UsuarioUpdate) -> Optional[Usuario]:
        """ Atualiza um usuário, tratando a troca de email e unicidade. """
        
        # Lógica de negócio: verifica se o novo email já está em uso por outro
        new_email = user_data.new_username or user_data.email
        if new_email and new_email != current_email:
            existing_user = await self.repo.get_user_by_email(new_email)
            if existing_user and existing_user.email != current_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Novo email já registrado por outro usuário."
                )

        return await self.repo.update_user(current_email, user_data)

    async def delete_user(self, email: str) -> bool:
        return await self.repo.delete_user(email)