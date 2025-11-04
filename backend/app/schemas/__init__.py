# backend/app/schemas/__init__.py
from .sistema import SistemaCreate, SistemaResponse, SistemaUpdate
from .modulo import ModuloCreate, ModuloResponse, ModuloUpdate
from .auth import Token, TokenData, LoginInput
from .usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse # <-- NOVO