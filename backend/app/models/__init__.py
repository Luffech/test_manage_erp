# backend/app/models/__init__.py
# Importa todos os modelos para serem reconhecidos pelo Alembic
from .caso_teste import CasoTeste
from .ciclo_teste import CicloTeste
from .metrica import Metrica
from .modulo import Modulo
from .nivel_acesso import NivelAcesso
from .projeto import Projeto
from .registro_tentativa_teste import RegistroTentativaTeste
from .sistema import Sistema
from .usuario import Usuario