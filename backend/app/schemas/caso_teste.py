# backend/app/schemas/caso_teste.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Sequence
from app.core.enums import PrioridadeCasoTesteEnum # <-- IMPORTA O ENUM PYTHON

# ----------------- PROJETO (Simplificado para Resposta) -----------------
class ProjetoResponse(BaseModel):
    id: int
    nome: str
    modulo_id: int
    sistema_id: int
    
    model_config = ConfigDict(from_attributes=True)

# ----------------- CASO TESTE -----------------
class CasoTesteBase(BaseModel):
    # Foreign keys
    projeto_id: int

    # Attributes
    nome: str
    descricao: Optional[str] = None
    passos: Optional[str] = None
    criterios_aceitacao: Optional[str] = None
    # CORREÇÃO: Usa o Enum Python e seu valor padrão
    prioridade: PrioridadeCasoTesteEnum = PrioridadeCasoTesteEnum.media

class CasoTesteCreate(CasoTesteBase):
    pass

class CasoTesteUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    passos: Optional[str] = None
    criterios_aceitacao: Optional[str] = None
    prioridade: Optional[PrioridadeCasoTesteEnum] = None
    ativo: Optional[bool] = None 

class CasoTesteResponse(CasoTesteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    projeto_nome: str
    ativo: bool
    
    model_config = ConfigDict(from_attributes=True)
    
# ----------------- REGISTRO TENTATIVA -----------------
class RegistroTentativaTesteResponse(BaseModel):
    id: int
    caso_teste_id: int
    usuario_id: int
    numero_tentativa: int
    resultado: bool 
    evidencias: Optional[str] = None
    data_execucao: datetime
    
    # Relationship fields
    caso_teste_nome: str
    usuario_nome: str
    
    model_config = ConfigDict(from_attributes=True)