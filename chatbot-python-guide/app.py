"""
API FastAPI do PythonGuide AI.
"""

from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag_engine import RAGEngine


# DIRETÓRIOS

Path("static").mkdir(
    exist_ok=True
)

Path("templates").mkdir(
    exist_ok=True
)


# FASTAPI

app = FastAPI(
    title="PythonGuide AI API",
    description=(
        "Chatbot com RAG, LangGraph, "
        "FAISS e LLM externa."
    ),
    version="2.0.0",
)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# FRONTEND

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static",
)


# RAG ENGINE

print(
    "\nInicializando PythonGuide AI..."
)

rag_engine = RAGEngine()

print(
    "\nPythonGuide AI pronto para uso."
)


# MODELOS DA API


class ChatRequest(BaseModel):

    message: str

    history: Optional[
        List[Dict[str, str]]
    ] = None


class ChatResponse(BaseModel):

    response: str


# ROTAS


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def root():

    template_path = (
        Path("templates")
        / "index.html"
    )

    return HTMLResponse(
        content=template_path.read_text(
            encoding="utf-8"
        )
    )


@app.get("/health")
async def health_check():

    return {
        "status": "online",
        "message": (
            "PythonGuide AI está funcionando."
        ),
    }


@app.get("/info")
async def get_info():

    return rag_engine.get_info()


@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat_endpoint(
    request: ChatRequest,
):

    try:

        if not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "A mensagem não pode "
                    "estar vazia."
                ),
            )

        response = rag_engine.chat(
            message=request.message,
            history=request.history or [],
        )

        return ChatResponse(
            response=response
        )

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"[ERRO] /chat: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Erro ao processar a "
                "mensagem."
            ),
        )


# EXECUÇÃO DIRETA


if __name__ == "__main__":

    import uvicorn

    print("\n" + "=" * 60)
    print("PYTHONGUIDE AI")
    print("=" * 60)

    info = rag_engine.get_info()

    print(
        f"Documentos: "
        f"{info['documents_total']}"
    )

    print(
        f"Chunks: "
        f"{info['chunks_total']}"
    )

    print(
        f"Modelo de embeddings: "
        f"{info['embedding_model']}"
    )

    print(
        f"Banco vetorial: "
        f"{info['vector_database']}"
    )

    print(
        f"Orquestração: "
        f"{info['orchestration']}"
    )

    print(
        f"LLM: "
        f"{info['llm_provider']} / "
        f"{info['llm_model']}"
    )

    print(
        "Aplicação: "
        "http://localhost:8000"
    )

    print(
        "Swagger: "
        "http://localhost:8000/docs"
    )

    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )