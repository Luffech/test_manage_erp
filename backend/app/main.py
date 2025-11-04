# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.api.v1.api import api_router

# Cria a aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)

# 1. Configura para servir arquivos estáticos (CSS, JS, Imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 2. Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclui o roteador principal da v1
app.include_router(api_router, prefix=settings.API_V1_STR)


# 4. Rotas que servem as páginas HTML (Substituindo as rotas do Flask)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_hub(request: Request):
    return templates.TemplateResponse("admin-dashboard.html", {"request": request})

@app.get("/admin/tests", response_class=HTMLResponse, include_in_schema=False)
async def admin_tests_page(request: Request):
    return templates.TemplateResponse("admin-tests.html", {"request": request})

@app.get("/admin/users", response_class=HTMLResponse, include_in_schema=False)
async def admin_users_page(request: Request):
    return templates.TemplateResponse("admin-users.html", {"request": request})

@app.get("/admin/metrics", response_class=HTMLResponse, include_in_schema=False)
async def admin_metrics_page(request: Request):
    return templates.TemplateResponse("admin-metrics.html", {"request": request})

@app.get("/tester-dashboard.html", response_class=HTMLResponse, include_in_schema=False)
async def tester_dashboard_page(request: Request):
    return templates.TemplateResponse("tester-dashboard.html", {"request": request})

# 5. Endpoints de Saúde (mantidos)
@app.get("/health", summary="Verifica a saúde da API")
def health_check():
    return {"status": "healthy"}