# backend/app/api/v1/endpoints/tester.py
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession # <-- LINHA ADICIONADA
from app.api.v1.deps import require_tester, get_current_active_user
from app.models import Usuario, CasoTeste
from app.schemas import CasoTesteResponse
from app.services.tester_service import TesterService
from .sistemas import get_db_session

router = APIRouter()

def get_tester_service(db: AsyncSession = Depends(get_db_session)) -> TesterService:
    return TesterService(db)

@router.get("/tests", response_model=Sequence[CasoTesteResponse], 
            summary="Listar testes ativos para execução (Tester)",
            dependencies=[Depends(require_tester)])
async def get_active_tests(
    service: TesterService = Depends(get_tester_service)
):
    """ Retorna a lista de Casos de Teste disponíveis para o testador. """
    return await service.get_active_tests()

@router.post("/execute", status_code=status.HTTP_200_OK, 
             summary="Executar um caso de teste (Simulação SAP)",
             dependencies=[Depends(require_tester)])
async def execute_test(
    data: dict, # Espera { "id": caso_teste_id, "cycles": num_cycles }
    current_user: Usuario = Depends(get_current_active_user),
    service: TesterService = Depends(get_tester_service)
):
    """ Simula a execução de um Caso de Teste para N ciclos e registra os resultados. """
    caso_teste_id = data.get("id")
    cycles = data.get("cycles")
    
    if not caso_teste_id or not cycles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do teste e ciclos são obrigatórios.")
    
    # O service se encarrega de registrar os N ciclos no DB
    return await service.execute_test(caso_teste_id=int(caso_teste_id), 
                                     usuario_id=current_user.id, 
                                     cycles=int(cycles))

@router.get("/results", summary="Meus resultados (Tester)")
async def get_my_results(
    current_user: Usuario = Depends(get_current_active_user),
    service: TesterService = Depends(get_tester_service)
):
    """ Retorna o histórico de execuções do usuário logado e sua taxa de sucesso. """
    return await service.get_my_results(current_user.id)