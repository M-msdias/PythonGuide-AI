"""
Engine RAG com LangGraph para orquestração do chatbot
"""

from typing import List, Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from knowledge_base import criar_base_conhecimento


class ChatState(TypedDict):
    message: str
    context: List[Document]
    history: List[Dict[str, str]]
    response: str


class RAGEngine:
    def __init__(self):
        """Inicializa a engine RAG"""
        print("Inicializando RAG Engine...")

        self.documentos, self.chunks = criar_base_conhecimento()
        print(f"{len(self.chunks)} chunks criados")

        print("Carregando embeddings (pode levar 1-2 minutos na primeira vez)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = FAISS.from_documents(self.chunks, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        self.app = self._build_graph()

    def _retrieve_context(self, state: ChatState) -> ChatState:
        """Recupera documentos relevantes"""
        docs = self.retriever.invoke(state["message"])
        state["context"] = docs
        print(f"📖 Recuperados {len(docs)} documentos")
        return state

    def _generate_response(self, state: ChatState) -> ChatState:
        """Gera resposta baseada no contexto"""
        if not state["context"]:
            state[
                "response"
            ] = """Não encontrei informações específicas sobre isso na minha base de conhecimento.

 **Sugestões:**
• Reformule sua pergunta de forma mais específica
• Pergunte sobre: Python, Machine Learning, Deep Learning, RAG, LangGraph, FastAPI
• Posso ajudar com conceitos de programação, IA e desenvolvimento web

O que mais gostaria de saber?"""
            return state

        context_text = "\n\n".join([doc.page_content for doc in state["context"]])

        main_info = context_text[:500]

        history_text = ""
        for msg in state["history"][-4:]:
            role = "Usuário" if msg["role"] == "user" else "Assistente"
            history_text += f"{role}: {msg['content']}\n"

        response = f"""📜 *Pergaminho Mágico Desvendado*

{main_info}

---

🔮 **Sobre sua consulta ao Oráculo:**
Encontrei {len(state['context'])} pergaminhos antigos relacionados ao seu questionamento nos arquivos da Biblioteca de Hogwarts.

⚡ **Conhecimentos que posso compartilhar com você:**
• 🦁 As quatro casas de Hogwarts (Grifinória, Sonserina, Corvinal e Lufa-Lufa)
• 🧙 Personagens do mundo bruxo (Harry, Hermione, Dumbledore, Snape, Voldemort)
• ✨ Feitiços e poções mágicas (Expecto Patronum, Avada Kedavra, Poção Polissuco)
• 🐉 Criaturas fantásticas (Dragões, Hipogrifos, Dementadores, Basilisco)
• 📚 Os livros e filmes da saga Harry Potter
• 🏰 Lugares mágicos (Hogwarts, Beco Diagonal, Azkaban, Toca)
• 👑 Relíquias da Morte e objetos mágicos (Varinha das Varinhas, Capa da Invisibilidade)
• ⚡ O esporte da Quadribol e suas regras

💫 *"A ajuda será sempre concedida em Hogwarts para aqueles que a merecem"* - Alvo Dumbledore

Deseja saber mais sobre algum desses temas do mundo bruxo?"""

        state["response"] = response
        return state

    def _build_graph(self):
        """Constrói o grafo do LangGraph"""
        workflow = StateGraph(ChatState)

        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)

        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def chat(self, message: str, history: List[Dict[str, str]] = None) -> str:
        """Processa uma mensagem e retorna a resposta"""
        if history is None:
            history = []

        state = ChatState(message=message, context=[], history=history, response="")

        result = self.app.invoke(state)
        return result["response"]

    def get_info(self):
        """Retorna informações sobre a engine"""
        return {
            "chunks_total": len(self.chunks),
            "documents_total": len(self.documentos),
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "status": "active",
        }
