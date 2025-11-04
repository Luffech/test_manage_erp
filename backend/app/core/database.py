# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Cria a engine assíncrona
engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

# Cria a fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
)

# Base para os nossos modelos ORM
Base = declarative_base()