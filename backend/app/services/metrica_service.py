# backend/app/services/metrica_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Sequence
from app.models import CasoTeste, RegistroTentativaTeste, Usuario
from sqlalchemy import Integer # Necessário para func.cast

class MetricaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overall_metrics(self) -> dict:
        """ Calcula métricas gerais de sucesso por teste/usuário. """

        # 1. Agregação Geral (Overall)
        total_runs_result = await self.db.execute(
            select(
                func.sum(func.cast(RegistroTentativaTeste.resultado, Integer)).label("successes"),
                func.count(RegistroTentativaTeste.id).label("total")
            )
        )
        total_data = total_runs_result.first()
        total_successes = total_data.successes or 0
        total_runs = total_data.total or 0
        overall_rate = round((total_successes / total_runs) * 100, 1) if total_runs > 0 else 0

        # 2. Agregação por Caso de Teste (Per Test)
        per_test_query = select(
            CasoTeste.nome.label("test_name"),
            func.sum(func.cast(RegistroTentativaTeste.resultado, Integer)).label("successes"),
            (func.count(RegistroTentativaTeste.id)).label("total_runs")
        ).join(RegistroTentativaTeste, RegistroTentativaTeste.caso_teste_id == CasoTeste.id
        ).group_by(CasoTeste.nome)
        
        per_test_results = (await self.db.execute(per_test_query)).fetchall()
        
        per_test_data = []
        for r in per_test_results:
            failures = r.total_runs - r.successes
            success_rate = round((r.successes / r.total_runs) * 100, 1) if r.total_runs > 0 else 0
            per_test_data.append({
                "test_name": r.test_name,
                "success_rate": success_rate,
                "total_runs": r.total_runs,
                "total_cycles": r.total_runs # Para o frontend, total_cycles é o total de runs
            })


        # 3. Agregação por Usuário (Per User)
        per_user_query = select(
            Usuario.email.label("username"),
            func.sum(func.cast(RegistroTentativaTeste.resultado, Integer)).label("successes"),
            (func.count(RegistroTentativaTeste.id)).label("total_runs")
        ).join(RegistroTentativaTeste, RegistroTentativaTeste.usuario_id == Usuario.id
        ).group_by(Usuario.email)

        per_user_results = (await self.db.execute(per_user_query)).fetchall()
        
        per_user_data = []
        for r in per_user_results:
            success_rate = round((r.successes / r.total_runs) * 100, 1) if r.total_runs > 0 else 0
            per_user_data.append({
                "username": r.username,
                "success_rate": success_rate,
                "runs": r.total_runs,
                "total_cycles": r.total_runs # Para o frontend, total_cycles é o total de runs
            })

        return {
            "overall_success_rate": overall_rate,
            "per_test": per_test_data,
            "per_user": per_user_data
        }