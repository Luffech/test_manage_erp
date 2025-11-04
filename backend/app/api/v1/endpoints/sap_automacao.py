# backend/app/api/v1/endpoints/sap_automacao.py
from fastapi import APIRouter, Depends, Body
from app.services.sap_service import SAPService, SAPLogin # SAPLogin é o schema de entrada

router = APIRouter()

# Instancia o serviço (sem injeção de DB, pois ele só conecta ao SAP)
sap_service = SAPService()

@router.post("/automar-sap", tags=["SAP"])
async def automar_sap(
    login_data: SAPLogin = Body(...)
):
    """
    Endpoint para iniciar uma automação SAP.
    Recebe login/senha no corpo da requisição.
    """
    return await sap_service.run_sap_automation(login_data)