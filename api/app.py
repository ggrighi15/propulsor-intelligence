from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .inicializar_app import inicializar_app
from .painel import render_painel

app = FastAPI()

@app.on_event("startup")
def startup():
    inicializar_app()

@app.get("/")
def root():
    return {"status": "OK", "message": "Propulsor rodando com sucesso"}

@app.get("/painel", response_class=HTMLResponse)
def painel():
    return render_painel()

@app.post("/executar-tarefa")
async def executar_tarefa(request: Request):
    body = await request.json()
    tarefa = body.get("tarefa")
    if tarefa == "distribuir_emails":
        from .distribuidor_emails import distribuir_emails
        distribuir_emails()
        return {"status": "ok", "executado": tarefa}
    return {"status": "erro", "mensagem": "Tarefa não reconhecida"}
