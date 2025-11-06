# backend/app/core/enums.py
import enum

# O Pydantic usará esta classe
class NivelAcessoEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

# O Pydantic usará esta classe
class PrioridadeCasoTesteEnum(str, enum.Enum):
    alta = "alta"
    media = "media"
    baixa = "baixa"

# O Pydantic usará esta classe
class StatusCicloEnum(str, enum.Enum):
    planejado = "planejado"
    em_execucao = "em_execucao"
    concluido = "concluido"
    pausado = "pausado"
    cancelado = "cancelado"
    erro = "erro"

# O Pydantic usará esta classe
class StatusProjetoEnum(str, enum.Enum):
    ativo = "ativo"
    pausado = "pausado"
    finalizado = "finalizado"

# O Pydantic usará esta classe
class TipoMetricaEnum(str, enum.Enum):
    cobertura = "cobertura"
    eficiencia = "eficiencia"
    defeitos = "defeitos"
    qualidade = "qualidade"
    produtividade = "produtividade"