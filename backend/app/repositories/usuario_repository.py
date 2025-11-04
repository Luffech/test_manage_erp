# backend/app/repositories/usuario_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from typing import Sequence, Optional
from app.core.security import get_password_hash 

from app.models import Usuario, NivelAcesso
from app.schemas import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UsuarioCreate) -> Usuario:
        """ Cria um novo registo de Usuário, hasheando a senha. """
        
        hashed_password = get_password_hash(user_data.password)
        
        user_data_dict = user_data.model_dump(exclude={'password'})
        
        db_user = Usuario(
            **user_data_dict,
            senha_hash=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        # Carrega o nível de acesso para a resposta
        await self.db.refresh(db_user, ['nivel_acesso']) 
        
        return db_user

    async def get_all_users(self) -> Sequence[Usuario]:
        """ Retorna todos os registos de Usuário, juntando o Nível de Acesso. """
        query = select(Usuario).join(NivelAcesso)
        result = await self.db.execute(query)
        # O scalars().unique().all() previne duplicatas ao usar join
        return result.scalars().unique().all() 

    async def get_user_by_email(self, email: str) -> Usuario | None:
        """ Retorna um único registo de Usuário pelo seu Email. """
        result = await self.db.execute(
            select(Usuario).where(Usuario.email == email)
        )
        return result.scalars().first()

    async def update_user(self, current_email: str, user_data: UsuarioUpdate) -> Optional[Usuario]:
        """ Atualiza um registo de Usuário. """
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Extrai o 'new_username' se existir (que será o novo email)
        new_email = update_data.pop('new_username', None) or update_data.pop('email', None)
        
        if new_email:
            update_data['email'] = new_email
        
        if not update_data:
            return await self.get_user_by_email(current_email)

        query = (
            sqlalchemy_update(Usuario)
            .where(Usuario.email == current_email)
            .values(**update_data)
            .returning(Usuario)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        
        updated_user = result.scalars().first()
        if updated_user:
             await self.db.refresh(updated_user, ['nivel_acesso']) 
        
        return updated_user

    async def delete_user(self, email: str) -> bool:
        """ Apaga um registo de Usuário pelo email. """
        query = sqlalchemy_delete(Usuario).where(Usuario.email == email)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0