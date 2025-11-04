# backend/app/schemas/sistema.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Schema base com os campos comuns
class SistemaBase(BaseModel):
    nome: str
    descricao: str | None = None

# Schema para a criação de um novo Sistema
class SistemaCreate(SistemaBase):
    pass 

class SistemaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

# Schema para a resposta da API
class SistemaResponse(SistemaBase):
    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime

    # Configuração para que o Pydantic consiga ler os dados de um objeto SQLAlchemy
    model_config = ConfigDict(from_attributes=True)