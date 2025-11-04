# backend/app/models/ciclo_teste.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# O nome do ENUM DEVE ser o mesmo definido em db/init.sql
status_ciclo_enum = ENUM('planejado', 'em_execucao', 'concluido', 'pausado', 'cancelado', 'erro', name='status_ciclo_enum', create_type=False)

class CicloTeste(Base):
    __tablename__ = "ciclos_teste"

    id = Column(Integer, primary_key=True, index=True)
    casos_teste_id = Column(Integer, ForeignKey("casos_teste.id"), nullable=False)
    nome = Column(String(255))
    numero = Column(Integer)
    descricao = Column(Text)
    data_inicio = Column(TIMESTAMP(timezone=True))
    data_fim = Column(TIMESTAMP(timezone=True))
    status = Column(status_ciclo_enum, default='planejado')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    caso_teste = relationship("CasoTeste", back_populates="ciclos_teste", foreign_keys=[casos_teste_id])
    metricas = relationship("Metrica", back_populates="ciclo_teste", foreign_keys="[Metrica.ciclo_teste_id]")