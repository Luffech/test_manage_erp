#!/bin/sh
set -e
set -x

echo "Iniciando processo de migração..."

# 1. Aplica migrações existentes primeiro
echo "Aplicando migrações existentes..."
alembic upgrade head

# 2. Verifica se PRECISA gerar nova migração
echo "Verificando se modelos foram atualizados..."
if alembic check; then
    echo "Nenhuma mudança detectada nos modelos."
else
    echo "Mudanças detectadas! Gerando nova migração..."
    # Gera uma nova migração com base nas mudanças do modelo
    alembic revision --autogenerate -m "Auto: $(date '+%Y-%m-%d %H:%M')"
    
    echo "Aplicando nova migração..."
    alembic upgrade head
    echo "Migração automática concluída!"
fi

echo "Iniciando aplicação..."
# Executa o comando principal do Dockerfile (uvicorn)
exec "$@"