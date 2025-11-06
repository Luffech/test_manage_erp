# backend/app/api/v1/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.usuario import Usuario
from app.core.enums import NivelAcessoEnum

from .endpoints.sistemas import get_db_session # Reutiliza a dependência da sessão

# Define o esquema de autenticação OAuth2 (usado para injeção de token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

# --- Funções de Injeção de Dependência ---

async def get_current_active_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # O subject 'sub' deve ser o email do usuário
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        # Busca o usuário no banco de dados
        result = await db.execute(
            select(Usuario).where(Usuario.email == email, Usuario.ativo == True)
        )
        user = result.scalars().first()
        
        if user is None:
            raise credentials_exception

        # Carrega o relacionamento nivel_acesso para que a role possa ser lida
        await db.refresh(user, ['nivel_acesso']) 
        
    except JWTError:
        raise credentials_exception
    
    return user

# --- Guards de Rota (Funções de Autorização) ---

def require_admin(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
    """ Exige que o usuário logado tenha o papel de 'admin'. """
    if current_user.nivel_acesso.nome != NivelAcessoEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    return current_user

def require_tester(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
    """ Exige que o usuário logado tenha o papel de 'tester' ou 'admin'. """
    role = current_user.nivel_acesso.nome.value
    if role not in (NivelAcessoEnum.admin.value, NivelAcessoEnum.user.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a testadores.")
    return current_user