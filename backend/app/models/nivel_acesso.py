# backend/app/models/nivel_acesso.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# O nome do ENUM DEVE ser o mesmo definido em db/init.sql
nivel_acesso_enum = ENUM('admin', 'user', name='nivel_acesso_enum', create_type=False)

class NivelAcesso(Base):
    __tablename__ = "niveis_acesso"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(nivel_acesso_enum, nullable=False)
    descricao = Column(Text)
    permissoes = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relacionamento: NivelAcesso.usuarios -> Usuario
    usuarios = relationship("Usuario", back_populates="nivel_acesso", foreign_keys="[Usuario.nivel_acesso_id]")