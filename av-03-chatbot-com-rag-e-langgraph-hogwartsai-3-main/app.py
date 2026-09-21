"""
API FastAPI para o Chatbot RAG com LangGraph
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
from rag_engine import RAGEngine

Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)


app = FastAPI(
    title="Chatbot RAG API",
    description="API para chatbot com RAG e LangGraph",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

print("Inicializando Chatbot RAG...")
rag_engine = RAGEngine()
print("Chatbot pronto para uso")


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    response: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve o front-end"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Verifica saúde da API"""
    return {
        "status": "online",
        "message": "Chatbot RAG API is running!",
        "timestamp": "2024-01-01T00:00:00Z",
    }


@app.get("/info")
async def get_info():
    """Retorna informações do chatbot"""
    return rag_engine.get_info()


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Endpoint para enviar mensagens ao chatbot"""
    try:
        response = rag_engine.chat(
            message=request.message, history=request.history or []
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("CHATBOT RAG COM LANGGRAPH")
    print("=" * 50)
    print(f"Base de conhecimento: {rag_engine.get_info()['chunks_total']} chunks")
    print(f"Servidor iniciado em: http://localhost:8000")
    print(f"Documentação da API: http://localhost:8000/docs")
    print("=" * 50)
    print("\nPressione CTRL+C para parar o servidor\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
