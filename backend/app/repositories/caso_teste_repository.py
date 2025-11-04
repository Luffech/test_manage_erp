# backend/app/repositories/caso_teste_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from typing import Sequence, Optional

from app.models import CasoTeste, Projeto
from app.schemas import CasoTesteCreate, CasoTesteUpdate

class CasoTesteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_caso_teste(self, caso_teste_data: CasoTesteCreate) -> CasoTeste:
        """ Cria um novo Caso de Teste. """
        db_obj = CasoTeste(
            **caso_teste_data.model_dump(),
            ativo=True, # Novo campo 'ativo'
            ciclo_teste_id=1 # MOCK: Assumindo ciclo_teste_id=1 como default, já que é NOT NULL no modelo
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get_all_casos_teste(self) -> Sequence[CasoTeste]:
        """ Retorna todos os Casos de Teste. """
        query = select(CasoTeste).order_by(CasoTeste.id) # Usamos ID para ordem padrão
        result = await self.db.execute(query)
        return result.scalars().all() 

    async def get_caso_teste_by_id(self, caso_teste_id: int) -> CasoTeste | None:
        """ Retorna um único Caso de Teste pelo ID. """
        result = await self.db.execute(
            select(CasoTeste).where(CasoTeste.id == caso_teste_id)
        )
        return result.scalars().first()

    async def update_caso_teste(self, caso_teste_id: int, caso_teste_data: CasoTesteUpdate) -> Optional[CasoTeste]:
        """ Atualiza um Caso de Teste. """
        update_data = caso_teste_data.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_caso_teste_by_id(caso_teste_id)

        query = (
            sqlalchemy_update(CasoTeste)
            .where(CasoTeste.id == caso_teste_id)
            .values(**update_data)
            .returning(CasoTeste)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        
        return result.scalars().first()

    async def delete_caso_teste(self, caso_teste_id: int) -> bool:
        """ Apaga um Caso de Teste. """
        query = sqlalchemy_delete(CasoTeste).where(CasoTeste.id == caso_teste_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0