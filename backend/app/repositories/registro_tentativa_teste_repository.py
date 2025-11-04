# backend/app/repositories/registro_tentativa_teste_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Sequence, Optional

from app.models import RegistroTentativaTeste, CasoTeste, Usuario

class RegistroTentativaTesteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_tentativa(self, caso_teste_id: int, usuario_id: int, resultado: bool, evidencias: Optional[str] = None) -> RegistroTentativaTeste:
        """ Adiciona um novo registro de tentativa de teste. """
        
        # Determina o número da tentativa (próximo número para este caso/usuário)
        subquery = select(func.max(RegistroTentativaTeste.numero_tentativa)).where(
            RegistroTentativaTeste.caso_teste_id == caso_teste_id,
            RegistroTentativaTeste.usuario_id == usuario_id
        )
        max_num_result = await self.db.execute(subquery)
        max_num = max_num_result.scalar() or 0
        
        db_obj = RegistroTentativaTeste(
            caso_teste_id=caso_teste_id,
            usuario_id=usuario_id,
            numero_tentativa=max_num + 1,
            resultado=resultado,
            evidencias=evidencias
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get_results_by_user(self, usuario_id: int) -> Sequence[RegistroTentativaTeste]:
        """ Retorna todos os resultados de teste para um usuário específico. """
        # JOINs necessários para obter o nome do CasoTeste e do Usuário (para serialização)
        query = select(RegistroTentativaTeste).where(
            RegistroTentativaTeste.usuario_id == usuario_id
        ).order_by(RegistroTentativaTeste.data_execucao.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()