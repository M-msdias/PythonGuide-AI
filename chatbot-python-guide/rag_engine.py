"""
Motor RAG utilizando LangGraph.

Fluxo:

PERGUNTA
   ↓
RECUPERAÇÃO
   ↓
MONTAGEM DO PROMPT
   ↓
LLM
   ↓
RESPOSTA
"""

import os
from typing import List, Dict, Any, TypedDict

from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq

from knowledge_base import criar_base_conhecimento


# VARIÁVEIS DE AMBIENTE

load_dotenv()


# ESTADO DO LANGGRAPH


class ChatState(TypedDict):
    """
    Estado compartilhado entre os nós do LangGraph.
    """

    message: str
    context: List[Document]
    history: List[Dict[str, str]]
    prompt: str
    response: str


# ENGINE


class RAGEngine:

    def __init__(self):

        print("\n" + "=" * 60)
        print("INICIALIZANDO PYTHONGUIDE AI")
        print("=" * 60)

        # BASE DE CONHECIMENTO

        self.documentos, self.chunks = (
            criar_base_conhecimento()
        )

        print(
            f"\n{len(self.chunks)} chunks preparados."
        )

        # EMBEDDINGS

        print(
            "\nCarregando modelo de embeddings..."
        )

        print(
            "Na primeira execução isso pode "
            "demorar alguns minutos."
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=(
                "sentence-transformers/"
                "all-MiniLM-L6-v2"
            ),
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

        # FAISS

        print(
            "\nCriando índice vetorial FAISS..."
        )

        self.vectorstore = (
            FAISS.from_documents(
                self.chunks,
                self.embeddings,
            )
        )

        self.retriever = (
            self.vectorstore.as_retriever(
                search_kwargs={
                    "k": 5
                }
            )
        )

        # LLM

        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY não encontrada. "
                "Crie um arquivo .env com sua "
                "chave da Groq."
            )

        model_name = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b",
        )

        print(
            f"\nCarregando LLM Groq: "
            f"{model_name}"
        )

        self.llm = ChatGroq(
            model=model_name,
            temperature=0.2,
            max_tokens=1200,
            api_key=api_key,
        )

        # PROMPT

        self.prompt_template = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
Você é o PythonGuide AI, um assistente
especializado em Python.

Sua função é responder perguntas sobre Python
utilizando PRINCIPALMENTE o contexto recuperado
da base de conhecimento.

REGRAS IMPORTANTES:

1. Responda em português do Brasil.

2. Utilize as informações presentes no contexto
   recuperado sempre que forem suficientes.

3. Não invente informações que não estejam
   sustentadas pelo contexto.

4. Se a informação não estiver disponível no
   contexto, diga claramente que ela não foi
   encontrada na base de conhecimento.

5. Você pode usar seu conhecimento geral apenas
   para explicar ou organizar uma informação que
   esteja sustentada pelo contexto.

6. Não finja que pesquisou na internet durante
   a conversa.

7. Considere o histórico da conversa para entender
   perguntas que dependam de mensagens anteriores.

8. Quando apresentar código Python, utilize
   blocos de código Markdown.

9. Explique conceitos de maneira didática,
   adequada para estudantes e desenvolvedores
   iniciantes.

10. Seja objetivo, mas forneça exemplos quando
    eles ajudarem na compreensão.

CONTEXTO RECUPERADO:
--------------------
{context}
--------------------

HISTÓRICO DA CONVERSA:
--------------------
{history}
--------------------
""",
                    ),
                    (
                        "human",
                        "{question}",
                    ),
                ]
            )
        )

        # LANGGRAPH

        self.app = self._build_graph()

        print("\n" + "=" * 60)
        print("PYTHONGUIDE AI PRONTO")
        print("=" * 60)

    # NÓ 1 — RECUPERAÇÃO

    def _retrieve_context(
        self,
        state: ChatState,
    ) -> ChatState:

        print(
            "\n[LANGGRAPH] Recuperando contexto..."
        )

        question = state["message"]

        docs = self.retriever.invoke(
            question
        )

        state["context"] = docs

        print(
            f"[LANGGRAPH] "
            f"{len(docs)} chunks recuperados."
        )

        return state

    # NÓ 2 — MONTAGEM DO PROMPT

    def _build_prompt(
        self,
        state: ChatState,
    ) -> ChatState:

        print(
            "[LANGGRAPH] Montando prompt..."
        )

        context_text = "\n\n".join(
            [
                (
                    f"DOCUMENTO {index + 1}\n"
                    f"{doc.page_content}"
                )
                for index, doc in enumerate(
                    state["context"]
                )
            ]
        )

        if not context_text:
            context_text = (
                "Nenhum contexto relevante "
                "foi recuperado."
            )

        # HISTÓRICO

        history_items = []

        for message in state[
            "history"
        ][-6:]:

            role = message.get(
                "role",
                "user",
            )

            content = message.get(
                "content",
                "",
            )

            if role == "user":
                role_name = "Usuário"
            else:
                role_name = "Assistente"

            history_items.append(
                f"{role_name}: {content}"
            )

        history_text = "\n".join(
            history_items
        )

        if not history_text:
            history_text = (
                "Nenhuma mensagem anterior."
            )

        # PROMPT FINAL

        prompt_value = (
            self.prompt_template.invoke(
                {
                    "context": context_text,
                    "history": history_text,
                    "question": state[
                        "message"
                    ],
                }
            )
        )

        # Converte o prompt estruturado para texto somente para armazenar no estado.
        state["prompt"] = (
            prompt_value.to_string()
        )

        return state

    # NÓ 3 — GERAÇÃO

    def _generate_response(
        self,
        state: ChatState,
    ) -> ChatState:

        print(
            "[LANGGRAPH] Chamando LLM externa..."
        )


        # A LLM externa é chamada SOMENTE aqui.
        # Embeddings e recuperação são realizados localmente.

        prompt_value = (
            self.prompt_template.invoke(
                {
                    "context": "\n\n".join(
                        [
                            doc.page_content
                            for doc in state[
                                "context"
                            ]
                        ]
                    ),
                    "history": self._format_history(
                        state["history"]
                    ),
                    "question": state[
                        "message"
                    ],
                }
            )
        )

        result = self.llm.invoke(
            prompt_value
        )

        state["response"] = (
            result.content
            if isinstance(
                result.content,
                str,
            )
            else str(result.content)
        )

        print(
            "[LANGGRAPH] Resposta gerada."
        )

        return state

    # HISTÓRICO

    @staticmethod
    def _format_history(
        history: List[Dict[str, str]],
    ) -> str:

        if not history:
            return (
                "Nenhuma mensagem anterior."
            )

        lines = []

        for message in history[-6:]:

            role = message.get(
                "role",
                "user",
            )

            content = message.get(
                "content",
                "",
            )

            role_name = (
                "Usuário"
                if role == "user"
                else "Assistente"
            )

            lines.append(
                f"{role_name}: {content}"
            )

        return "\n".join(lines)

    # CONSTRUÇÃO DO GRAFO

    def _build_graph(self):

        workflow = StateGraph(
            ChatState
        )

        # Nós principais do RAG
        workflow.add_node(
            "retrieve",
            self._retrieve_context,
        )

        workflow.add_node(
            "build_prompt",
            self._build_prompt,
        )

        workflow.add_node(
            "generate",
            self._generate_response,
        )

        # Entrada
        workflow.set_entry_point(
            "retrieve"
        )

        # Fluxo
        workflow.add_edge(
            "retrieve",
            "build_prompt",
        )

        workflow.add_edge(
            "build_prompt",
            "generate",
        )

        workflow.add_edge(
            "generate",
            END,
        )

        return workflow.compile()

    # CHAT

    def chat(
        self,
        message: str,
        history: List[
            Dict[str, str]
        ] = None,
    ) -> str:

        if history is None:
            history = []

        state: ChatState = {
            "message": message,
            "context": [],
            "history": history,
            "prompt": "",
            "response": "",
        }

        result = self.app.invoke(
            state
        )

        return result[
            "response"
        ]

    # INFORMAÇÕES

    def get_info(self):

        return {
            "name": "PythonGuide AI",
            "domain": (
                "Python e documentação oficial"
            ),
            "documents_total": len(
                self.documentos
            ),
            "chunks_total": len(
                self.chunks
            ),
            "embedding_model": (
                "sentence-transformers/"
                "all-MiniLM-L6-v2"
            ),
            "vector_database": "FAISS",
            "orchestration": "LangGraph",
            "llm_provider": "Groq",
            "llm_model": os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-20b",
            ),
            "status": "active",
        }