from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .models import Base
from .database import engine

app = FastAPI(
    title="Cities Microservice",
    description="Master Data microservice for cities",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
