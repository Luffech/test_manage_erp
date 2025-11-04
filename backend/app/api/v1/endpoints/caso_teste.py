# backend/app/api/v1/endpoints/caso_teste.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.schemas import CasoTesteCreate, CasoTesteResponse, CasoTesteUpdate
from app.services.caso_teste_service import CasoTesteService
from app.api.v1.deps import require_admin
from .sistemas import get_db_session 

router = APIRouter()

def get_caso_teste_service(db: AsyncSession = Depends(get_db_session)) -> CasoTesteService:
    return CasoTesteService(db)

@router.post("/", response_model=CasoTesteResponse, status_code=status.HTTP_201_CREATED, 
             summary="Criar um novo Caso de Teste (Admin)",
             dependencies=[Depends(require_admin)])
async def create_caso_teste(
    caso_teste: CasoTesteCreate,
    service: CasoTesteService = Depends(get_caso_teste_service)
):
    """ Cria um novo Caso de Teste na base de dados. """
    return await service.create_caso_teste(caso_teste)

@router.get("/", response_model=Sequence[CasoTesteResponse], 
            summary="Listar todos os Casos de Teste (Admin)",
            dependencies=[Depends(require_admin)])
async def get_casos_teste(
    service: CasoTesteService = Depends(get_caso_teste_service)
):
    """ Retorna uma lista de todos os Casos de Teste. """
    return await service.get_all_casos_teste()

@router.put("/{caso_teste_id}", response_model=CasoTesteResponse, 
            summary="Atualizar um Caso de Teste por ID (Admin)",
            dependencies=[Depends(require_admin)])
async def update_caso_teste(
    caso_teste_id: int,
    caso_teste_data: CasoTesteUpdate,
    service: CasoTesteService = Depends(get_caso_teste_service)
):
    """ Atualiza as informações de um Caso de Teste existente. """
    updated_obj = await service.update_caso_teste(caso_teste_id, caso_teste_data)
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Caso de Teste não encontrado")
    return updated_obj

@router.delete("/{caso_teste_id}", status_code=status.HTTP_204_NO_CONTENT, 
               summary="Apagar um Caso de Teste por ID (Admin)",
               dependencies=[Depends(require_admin)])
async def delete_caso_teste(
    caso_teste_id: int,
    service: CasoTesteService = Depends(get_caso_teste_service)
):
    """ Apaga um Caso de Teste da base de dados. """
    success = await service.delete_caso_teste(caso_teste_id)
    if not success:
        raise HTTPException(status_code=404, detail="Caso de Teste não encontrado")
    return 

# Rota para simular a reordenação do Frontend
@router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT, 
             summary="Reordenar Casos de Teste (Admin)",
             dependencies=[Depends(require_admin)])
async def reorder_casos_teste(
    ordered_ids: Sequence[int],
    service: CasoTesteService = Depends(get_caso_teste_service)
):
    """ Simula a reordenação dos Casos de Teste. """
    await service.reorder_casos_teste(ordered_ids)
    return