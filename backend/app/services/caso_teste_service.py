# backend/app/services/caso_teste_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from app.models import CasoTeste, Projeto
from app.repositories.caso_teste_repository import CasoTesteRepository
from app.schemas import CasoTesteCreate, CasoTesteUpdate

class CasoTesteService:
    def __init__(self, db: AsyncSession):
        self.repo = CasoTesteRepository(db)
        self.db = db

    async def create_caso_teste(self, caso_teste_data: CasoTesteCreate) -> CasoTeste:
        """ Cria um caso de teste, validando o projeto_id. """
        
        # Validação do projeto_id (se existe)
        projeto_result = await self.db.execute(
            select(Projeto).where(Projeto.id == caso_teste_data.projeto_id)
        )
        if not projeto_result.scalars().first():
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Projeto com ID {caso_teste_data.projeto_id} não encontrado."
            )

        return await self.repo.create_caso_teste(caso_teste_data)

    async def get_all_casos_teste(self) -> Sequence[CasoTeste]:
        return await self.repo.get_all_casos_teste()

    async def update_caso_teste(self, caso_teste_id: int, caso_teste_data: CasoTesteUpdate) -> Optional[CasoTeste]:
        return await self.repo.update_caso_teste(caso_teste_id, caso_teste_data)

    async def delete_caso_teste(self, caso_teste_id: int) -> bool:
        return await self.repo.delete_caso_teste(caso_teste_id)
    
    async def reorder_casos_teste(self, ordered_ids: Sequence[int]) -> bool:
        """ Simula a reordenação. """
        # MOCK: Apenas retorna True. No real, usaria UPDATEs sequenciais no BD.
        return True