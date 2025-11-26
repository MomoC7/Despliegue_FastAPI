from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from . import models
from .database import engine

app = FastAPI(
    title="Auth Service",
    description="Servicio de autenticación para DidiFood",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}