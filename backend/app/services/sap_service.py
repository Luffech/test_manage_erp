# backend/app/services/sap_service.py
from pydantic import BaseModel
from fastapi import HTTPException

# Modelo para receber os dados da requisição
class SAPLogin(BaseModel):
    user: str
    passwd: str

class SAPService:
    def __init__(self):
        # ATENÇÃO: Substitua pelos dados de conexão do seu servidor SAP
        self.sap_params = {
            'ashost': 'SEU_SERVIDOR_SAP.com', 
            'sysnr': '00',                    
            'client': '100',                  
            'lang': 'PT'
        }

    async def run_sap_automation(self, login_data: SAPLogin):
        """ Conecta ao SAP usando RFC e executa uma função (BAPI). """
        try:
            # Importa o 'pyrfc' somente quando o endpoint é chamado
            from pyrfc import Connection, ABAPApplicationError, CommunicationError
        except ImportError:
            raise HTTPException(
                status_code=501, 
                detail="Integração SAP não instalada. O backend foi buildado sem a flag 'WITH_SAP=true'."
            )

        try:
            # 1. Conecta ao SAP
            conn = Connection(
                user=login_data.user,
                passwd=login_data.passwd,
                **self.sap_params
            )

            # 2. Executa a função RFC (BAPI de exemplo)
            result = conn.call(
                "BAPI_USER_GET_DETAIL",
                USERNAME=login_data.user
            )
            
            # 3. Fecha a conexão
            conn.close()
            
            return {
                "message": "Automação SAP executada com sucesso!",
                "dados_retornados": result.get('ADDRESS')
            }

        except CommunicationError as e:
            raise HTTPException(status_code=500, detail=f"Erro de Comunicação SAP: {e}")
        except ABAPApplicationError as e:
            raise HTTPException(status_code=400, detail=f"Erro de Aplicação SAP: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")