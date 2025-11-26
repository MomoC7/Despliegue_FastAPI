from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .models import Base
from .database import engine

app = FastAPI(
    title="Categories Microservice",
    description="Master Data microservice for event categories",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Rutas
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
