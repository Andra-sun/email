from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.api.routes import email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para classificação de emails em Produtivo/Improdutivo"
)

# Configuração de CORS mais permissiva
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(
    email.router,
    prefix=settings.API_V1_STR
)

@app.get("/")
async def root():
    return {
        "message": f"Bem-vindo ao {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 {settings.APP_NAME} iniciando...")
    logger.info(f"Debug: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"🛑 {settings.APP_NAME} encerrado")