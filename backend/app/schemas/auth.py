# backend/app/schemas/auth.py
from pydantic import BaseModel
from typing import Any

# Formato do Token retornado ao cliente
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str # Incluímos o papel para facilitar a navegação no frontend

# Payload de dados dentro do Token (sub, role)
class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None
    id: int | None = None

# Input de login (o que a API espera no POST /login)
class LoginInput(BaseModel):
    username: str # Será usado como email
    password: str