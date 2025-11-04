# backend/app/schemas/caso_teste.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Sequence
from app.models.caso_teste import prioridade_enum # Assumindo que este ENUM está acessível

# ----------------- PROJETO (Simplificado para Resposta) -----------------
class ProjetoResponse(BaseModel):
    id: int
    nome: str
    modulo_id: int
    sistema_id: int
    
    model_config = ConfigDict(from_attributes=True)

# ----------------- CASO TESTE -----------------
class CasoTesteBase(BaseModel):
    # Foreign keys (temporariamente omitindo ciclo_teste_id para o CRUD inicial)
    projeto_id: int

    # Attributes
    nome: str
    descricao: Optional[str] = None
    passos: Optional[str] = None
    criterios_aceitacao: Optional[str] = None
    prioridade: prioridade_enum = prioridade_enum.media

class CasoTesteCreate(CasoTesteBase):
    pass

class CasoTesteUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    passos: Optional[str] = None
    criterios_aceitacao: Optional[str] = None
    prioridade: Optional[prioridade_enum] = None
    ativo: Optional[bool] = None # Adicionando status ativo para o frontend

class CasoTesteResponse(CasoTesteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Adicionar nome do projeto e status
    projeto_nome: str
    ativo: bool
    
    model_config = ConfigDict(from_attributes=True)
    
# ----------------- REGISTRO TENTATIVA -----------------
class RegistroTentativaTesteResponse(BaseModel):
    id: int
    caso_teste_id: int
    usuario_id: int
    numero_tentativa: int
    resultado: bool # True (success), False (failure)
    evidencias: Optional[str] = None
    data_execucao: datetime
    
    # Relationship fields
    caso_teste_nome: str
    usuario_nome: str
    
    model_config = ConfigDict(from_attributes=True)