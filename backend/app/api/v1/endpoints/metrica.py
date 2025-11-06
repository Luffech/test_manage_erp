# backend/app/api/v1/endpoints/metrica.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession # <-- LINHA ADICIONADA
from app.api.v1.deps import require_admin
from app.services.metrica_service import MetricaService
from .sistemas import get_db_session

router = APIRouter()

def get_metrica_service(db: AsyncSession = Depends(get_db_session)) -> MetricaService:
    return MetricaService(db)

@router.get("/", summary="Métricas gerais do sistema (Admin)",
            dependencies=[Depends(require_admin)])
async def get_metrics(
    service: MetricaService = Depends(get_metrica_service)
):
    """ Retorna KPIs gerais, por teste e por usuário. """
    return await service.get_overall_metrics()