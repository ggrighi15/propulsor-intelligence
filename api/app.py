from fastapi import FastAPI
from inicializar_app import inicializar_app

app = FastAPI()

@app.on_event("startup")
def startup():
    inicializar_app()

@app.get("/")
def root():
    return {"status": "OK", "message": "Propulsor rodando com sucesso"}
