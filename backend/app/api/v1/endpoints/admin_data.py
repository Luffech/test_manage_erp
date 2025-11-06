# backend/app/api/v1/endpoints/admin_data.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash
from app.models import Usuario, NivelAcesso
from app.core.enums import NivelAcessoEnum
from .sistemas import get_db_session

router = APIRouter()

@router.post("/seed", status_code=status.HTTP_201_CREATED, summary="[DEV] Cria Níveis de Acesso e Admin Inicial", include_in_schema=False)
async def seed_initial_data(db: AsyncSession = Depends(get_db_session)):
    
    # 1. Cria Níveis de Acesso (se não existirem)
    niveis_acesso = [
        {"nome": NivelAcessoEnum.admin, "descricao": "Acesso total ao sistema"},
        {"nome": NivelAcessoEnum.user, "descricao": "Acesso para executar testes (Testador)"},
    ]
    
    for na_data in niveis_acesso:
        result = await db.execute(select(NivelAcesso).where(NivelAcesso.nome == na_data['nome']))
        if result.scalars().first() is None:
            db.add(NivelAcesso(**na_data))
            
    await db.commit()
    
    # 2. Insere Usuário Admin Inicial (se não existir)
    admin_email = "admin@example.com"
    admin_password_raw = "adm123" 
    
    user_result = await db.execute(select(Usuario).where(Usuario.email == admin_email))
    if user_result.scalars().first() is None:
        
        # Busca o ID do NivelAcesso 'admin'
        admin_na_result = await db.execute(select(NivelAcesso).where(NivelAcesso.nome == NivelAcessoEnum.admin))
        admin_na = admin_na_result.scalars().first()
        
        if admin_na is None:
            raise HTTPException(status_code=500, detail="Nível de acesso 'admin' não encontrado após seed.")
        
        db.add(Usuario(
            nome="Administrador Inicial",
            email=admin_email,
            senha_hash=get_password_hash(admin_password_raw),
            nivel_acesso_id=admin_na.id,
            ativo=True
        ))
        await db.commit()
        
    return {"message": "Dados iniciais (Níveis de Acesso e Admin) criados com sucesso!"}