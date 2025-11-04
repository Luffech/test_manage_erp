# backend/app/schemas/usuario.py
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

# Base schema para leitura de dados
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    credential: Optional[str] = None
    department: Optional[str] = None
    birth_date: Optional[str] = None
    
class UsuarioCreate(UsuarioBase):
    # Senha para ser hasheada
    password: str
    # O nivel_acesso_id é obrigatório na criação
    nivel_acesso_id: int 
    
class UsuarioUpdate(BaseModel):
    # Permite alterar o username (email)
    new_username: Optional[EmailStr] = None 
    
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    credential: Optional[str] = None
    department: Optional[str] = None
    birth_date: Optional[str] = None
    ativo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    nivel_acesso_id: int
    created_at: datetime
    updated_at: datetime
    
    # Adicionamos o nome do nível de acesso para facilitar a exibição
    nivel_acesso_nome: str 

    model_config = ConfigDict(from_attributes=True)