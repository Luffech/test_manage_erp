# backend/app/services/auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token, LoginInput
from app.models.nivel_acesso import NivelAcesso 
from app.models.nivel_acesso import nivel_acesso_enum # Importa o ENUM para garantir o papel

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, credentials: LoginInput) -> Usuario | None:
        # 1. Buscar o usuário pelo email
        query = (
            select(Usuario)
            .where(Usuario.email == credentials.username)
        )
        result = await self.db.execute(query)
        user = result.scalars().first()

        if user is None or user.ativo is False:
            return None 

        # 2. Verificar o hash da senha
        if not verify_password(credentials.password, user.senha_hash):
            return None 

        # 3. Carregar o Nível de Acesso para obter o 'role'
        # O refresh garante que o relacionamento 'nivel_acesso' seja carregado
        await self.db.refresh(user, ['nivel_acesso'])
        
        return user
    
    def generate_token(self, user: Usuario) -> Token:
        role = user.nivel_acesso.nome.value 
        access_token = create_access_token(
            data={"sub": user.email, "role": role, "id": user.id} 
        )
        return Token(access_token=access_token, token_type="bearer", role=role)