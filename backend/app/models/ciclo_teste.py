# backend/app/models/ciclo_teste.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.enums import StatusCicloEnum # <-- IMPORTAR O ENUM PYTHON

# SQLAlchemy usará o Enum Python para criar seu tipo
status_ciclo_enum = ENUM(
    StatusCicloEnum, 
    name='status_ciclo_enum', 
    create_type=True
)

class CicloTeste(Base):
    __tablename__ = "ciclos_teste"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    numero = Column(Integer)
    descricao = Column(Text)
    data_inicio = Column(TIMESTAMP(timezone=True))
    data_fim = Column(TIMESTAMP(timezone=True))
    # CORREÇÃO: Usar o Enum Python para o valor padrão
    status = Column(status_ciclo_enum, default=StatusCicloEnum.planejado)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    casos_teste = relationship("CasoTeste", back_populates="ciclo_teste")
    metricas = relationship("Metrica", back_populates="ciclo_teste", foreign_keys="[Metrica.ciclo_teste_id]")