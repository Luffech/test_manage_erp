# backend/app/models/caso_teste.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums import PrioridadeCasoTesteEnum # <-- IMPORTAR O ENUM PYTHON

# SQLAlchemy usará o Enum Python para criar seu tipo
prioridade_enum = ENUM(
    PrioridadeCasoTesteEnum, 
    name='prioridade_caso_teste_enum', 
    create_type=True
)

class CasoTeste(Base):
    __tablename__ = "casos_teste"

    id = Column(Integer, primary_key=True, index=True)
    ciclo_teste_id = Column(Integer, ForeignKey("ciclos_teste.id"), nullable=True) 
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    passos = Column(Text)
    criterios_aceitacao = Column(Text)
    # CORREÇÃO: Usar o Enum Python para o valor padrão
    prioridade = Column(prioridade_enum, default=PrioridadeCasoTesteEnum.media)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    projeto = relationship("Projeto", back_populates="casos_teste", foreign_keys=[projeto_id])
    ciclo_teste = relationship("CicloTeste", back_populates="casos_teste", foreign_keys=[ciclo_teste_id])
    tentativas = relationship("RegistroTentativaTeste", back_populates="caso_teste", foreign_keys="[RegistroTentativaTeste.caso_teste_id]")