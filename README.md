# 🐍 PythonGuide AI

Chatbot web baseado em **RAG (Retrieval-Augmented Generation)** para responder perguntas sobre Python utilizando como base de conhecimento a documentação oficial da linguagem.

## 📌 Sobre o projeto

O projeto atende aos requisitos da atividade através de:

- **Interface web:** HTML, CSS e JavaScript;
- **Back-end:** Python + FastAPI;
- **RAG:** recuperação semântica utilizando embeddings e FAISS;
- **Orquestração:** LangGraph;
- **Base de conhecimento:** documentação oficial do Python;
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`;
- **Banco vetorial:** FAISS;
- **LLM externa:** Groq com `openai/gpt-oss-20b`;
- **Containerização:** Docker e Docker Compose.

A base de conhecimento possui **52 páginas coletadas, 79 documentos processados e 1.334 chunks**.

A LLM externa é utilizada exclusivamente na etapa de geração da resposta. A recuperação das informações é realizada pelo índice vetorial local.

---

## 🌐 Acesso à aplicação

A aplicação está disponível para demonstração através do GitHub Codespaces:

**[🐍 Acessar o PythonGuide AI](https://automatic-carnival-pjg4q7gv47jw27jwj-8000.app.github.dev/)**

> O link depende do GitHub Codespace estar ativo. Caso a aplicação não esteja disponível, siga as instruções de execução abaixo.

---

# 🚀 Como executar

## Pré-requisitos

- Git
- Docker
- Docker Compose
- Chave de API da Groq

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd chatbot-python-guide
```

## 2. Configurar a API da Groq

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=openai/gpt-oss-20b
```

> **Importante:** não publique sua chave da Groq no GitHub. O arquivo `.env` está incluído no `.gitignore`.

## 3. Executar com Docker

```bash
docker compose up --build
```

Aguarde a inicialização da aplicação. O servidor será executado na porta `8000`.

### GitHub Codespaces

Na aba **PORTS**:

1. Localize a porta `8000`;
2. Clique em **Open in Browser**.

### Execução local

Acesse:

```text
http://localhost:8000
```

---

# 🧪 Testando a aplicação

### Verificar se o servidor está funcionando

```bash
curl http://localhost:8000/health
```

### Consultar informações do sistema

```bash
curl http://localhost:8000/info
```

### Enviar uma pergunta

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"O que é uma lista em Python?"}'
```

Também é possível realizar as perguntas diretamente pela interface web.

---

# 📚 Base de conhecimento

A base foi construída a partir da documentação oficial do Python:

https://docs.python.org/pt-br/3/

O conteúdo é coletado, organizado, dividido em chunks, transformado em embeddings e armazenado em um índice FAISS para recuperação semântica.

---

# 🔄 Fluxo do RAG

```text
Pergunta do usuário
        ↓
     LangGraph
        ↓
Recuperação no FAISS
        ↓
Construção do contexto
        ↓
Montagem do prompt
        ↓
Groq / GPT-OSS-20B
        ↓
Resposta
```

O LangGraph organiza as principais etapas do processo:

```text
retrieve → build_prompt → generate → END
```

---

# 📁 Principais arquivos

```text
app.py              → API FastAPI e interface
knowledge_base.py   → coleta e preparação da base
rag_engine.py       → RAG, FAISS e LangGraph
data/               → cache da base de conhecimento
templates/          → interface HTML
static/             → estilos da interface
Dockerfile          → configuração do container
docker-compose.yml  → execução com Docker
requirements.txt    → dependências
```

## 👥 Atividade acadêmica

**Domínio:** Python e documentação técnica.

**Tecnologias principais:** Python, FastAPI, LangGraph, FAISS, Sentence Transformers, Groq, Docker e JavaScript.