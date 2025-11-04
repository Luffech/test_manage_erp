# backend/app/services/tester_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from fastapi import HTTPException, status
import random 

from app.models import CasoTeste, RegistroTentativaTeste
from app.repositories.registro_tentativa_teste_repository import RegistroTentativaTesteRepository
from app.schemas import RegistroTentativaTesteResponse

class TesterService:
    def __init__(self, db: AsyncSession):
        self.repo = RegistroTentativaTesteRepository(db)
        self.db = db

    async def get_active_tests(self) -> Sequence[CasoTeste]:
        """ Retorna Casos de Teste ativos (ativo=True). """
        result = await self.db.execute(select(CasoTeste).where(CasoTeste.ativo == True))
        return result.scalars().all()
    
    async def execute_test(self, caso_teste_id: int, usuario_id: int, cycles: int) -> dict:
        """ Simula a execução do teste e registra os resultados. """
        
        caso_teste = await self.db.get(CasoTeste, caso_teste_id)
        if not caso_teste or not caso_teste.ativo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caso de teste não encontrado ou inativo.")
        
        successes = 0
        failures = 0
        
        # Simulação: 70% de sucesso por ciclo
        for _ in range(cycles):
            resultado = random.random() < 0.7 
            if resultado:
                successes += 1
            else:
                failures += 1
                
            # REGISTRO DETALHADO: Grava uma entrada por ciclo
            await self.repo.add_tentativa(
                caso_teste_id, 
                usuario_id, 
                resultado, 
                f"Resultado do ciclo {_+1}: {'Sucesso' if resultado else 'Falha'}"
            )

        return {
            "caso_teste_id": caso_teste_id,
            "cycles": cycles,
            "successes": successes,
            "failures": failures
        }
        
    async def get_my_results(self, usuario_id: int) -> dict:
        """ Retorna os resultados e a taxa de sucesso agregada para o usuário. """
        
        results = await self.repo.get_results_by_user(usuario_id)
        
        # Cálculo de taxa de sucesso geral (para o KPI myRate)
        total_runs = len(results)
        total_successes = sum(1 for r in results if r.resultado)
        
        rate = round((total_successes / total_runs) * 100, 1) if total_runs > 0 else 0
        
        # Serializa os resultados. Precisamos preencher os campos de relacionamento.
        response_results = []
        for r in results:
            # Note: Para evitar consultas N+1, precisamos carregar os relacionamentos antes de serializar
            if r.caso_teste is None:
                await self.db.refresh(r, ['caso_teste']) 
                
            response_results.append({
                "id": r.id,
                "caso_teste_id": r.caso_teste_id,
                "usuario_id": r.usuario_id,
                "numero_tentativa": r.numero_tentativa,
                "resultado": r.resultado,
                "evidencias": r.evidencias,
                "data_execucao": r.data_execucao,
                "caso_teste_nome": r.caso_teste.nome if r.caso_teste else "N/A",
                "usuario_nome": "N/A" # O nome do usuário não está no modelo Registro, é pego do token
            })

        return {
            "my_success_rate": rate,
            "results": response_results 
        }