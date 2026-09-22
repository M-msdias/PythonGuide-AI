# 🐍 PythonGuide AI

Chatbot web desenvolvido para responder perguntas sobre Python utilizando uma arquitetura de RAG (Retrieval-Augmented Generation).

O projeto utiliza:

- Python
- FastAPI
- LangGraph
- LangChain
- FAISS
- Hugging Face Sentence Transformers
- Groq
- HTML
- CSS
- JavaScript
- Docker

---

# 1. Sobre o projeto

O PythonGuide AI é um chatbot especializado em Python.

A aplicação utiliza RAG para recuperar informações relevantes de uma base de conhecimento antes de solicitar à LLM a geração da resposta.

O objetivo é evitar que a LLM dependa exclusivamente de seu conhecimento interno e fornecer a ela contexto relacionado à pergunta do usuário.

---

# 2. Arquitetura

O fluxo principal da aplicação é:

Pergunta do usuário

↓

FastAPI

↓

LangGraph

↓

Recuperação dos documentos relevantes

↓

FAISS

↓

Montagem do contexto

↓

Histórico da conversa

↓

Montagem do prompt

↓

LLM externa

↓

Resposta

↓

Interface web

---

# 3. Base de conhecimento

O domínio escolhido para o projeto é:

Python e documentação técnica da linguagem.

A base utiliza:

- conteúdo introdutório sobre Python;
- documentação oficial;
- tutorial da linguagem;
- biblioteca padrão;
- referência da linguagem;
- módulos;
- estruturas de dados;
- funções;
- classes;
- exceções;
- arquivos;
- JSON;
- expressões regulares;
- datas;
- logging;
- asyncio;
- SQLite;
- testes;
- threading;
- subprocess;
- ambientes virtuais;
- entre outros.

O código realiza web scraping de diversas páginas da documentação oficial e transforma o conteúdo em documentos e posteriormente em chunks.

---

# 4. Pipeline RAG

O pipeline utilizado é:

## 4.1 Coleta

As páginas da documentação são obtidas através de requisições HTTP.

## 4.2 Limpeza

O conteúdo HTML é processado com BeautifulSoup.

Elementos como:

- scripts;
- estilos;
- navegação;
- cabeçalhos;
- rodapés;

são removidos.

## 4.3 Chunking

Os documentos são divididos em partes menores utilizando RecursiveCharacterTextSplitter.

Configuração utilizada:

- chunk_size: 900
- chunk_overlap: 150

## 4.4 Embeddings

Os chunks são convertidos em vetores utilizando:

sentence-transformers/all-MiniLM-L6-v2

Os embeddings são gerados localmente.

## 4.5 Banco vetorial

Os embeddings são armazenados em um índice FAISS.

## 4.6 Recuperação

Para cada pergunta do usuário são recuperados os 5 chunks mais relevantes.

## 4.7 Geração

Os chunks recuperados são enviados como contexto para uma LLM externa.

A LLM é utilizada somente na etapa de geração da resposta.

---

# 5. LangGraph

O fluxo do chatbot é orquestrado utilizando LangGraph.

O grafo possui três etapas principais:

retrieve
↓
build_prompt
↓
generate
↓
END

### retrieve

Recupera os documentos semanticamente relacionados à pergunta.

### build_prompt

Combina:

- pergunta atual;
- contexto recuperado;
- histórico da conversa.

### generate

Envia o prompt para a LLM externa e recebe a resposta.

---

# 6. LLM

A geração de respostas utiliza uma LLM hospedada pela Groq.

O modelo utilizado por padrão é:

openai/gpt-oss-20b

A chave de acesso deve ser configurada através da variável de ambiente:

GROQ_API_KEY

---

# 7. Estrutura do projeto

```text
.
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── rag_engine.py
├── knowledge_base.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md