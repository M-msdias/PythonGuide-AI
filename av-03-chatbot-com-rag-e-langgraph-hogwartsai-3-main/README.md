# HogawatsAI

API em FastAPI para um chatbot com RAG (Retrieval-Augmented Generation) usando LangGraph.

---

## Requisitos

### Sem Docker
- Python 3.10+
- `pip`
- (Opcional) ambiente virtual (`venv`)

### Com Docker
- Docker
- (Opcional) Docker Compose

---

## Como rodar sem Docker

1. Clonar o repositório (ou baixar o código) e entrar na pasta:

   ```bash
   cd av-03-chatbot-com-rag-e-langgraph-hogwartsai-3
   ```

2. (Opcional) Criar e ativar um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Iniciar a API (escolha uma das opções):

   ```bash
   # usando uvicorn direto
   uvicorn app:app --host 0.0.0.0 --port 8000

   # ou
   python app.py
   ```

5. Acessar no navegador:

   - Aplicação (front-end): `http://localhost:8000`
   - Documentação da API (Swagger): `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

---

## Como rodar com Docker

### 1. Usando Docker Compose (recomendado)

1. Na pasta do projeto:

   ```bash
   cd av03
   ```

2. Construir e subir o container:

   ```bash
   docker compose up --build
   # ou, dependendo da versão:
   docker-compose up --build
   ```

3. Acessar:

   - Aplicação: `http://localhost:8000`
   - Docs da API: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

4. Para parar os containers:

   ```bash
   docker compose down
   # ou
   docker-compose down
   ```

### 2. Usando apenas Docker

1. Construir a imagem:

   ```bash
   docker build -t chatbot-rag-langgraph .
   ```

2. Rodar o container:

   ```bash
   docker run --name chatbot-rag \
     -p 8000:8000 \
     --restart unless-stopped \
     chatbot-rag-langgraph
   ```

3. Acessar:

   - `http://localhost:8000`
   - `http://localhost:8000/docs`

---

## Endpoints principais

- `GET /`  
  Serve o front-end do chatbot.

- `GET /health`  
  Verifica o status da API.

- `GET /info`  
  Retorna informações do chatbot e da base de conhecimento.

- `POST /chat`  
  Endpoint principal para conversa com o chatbot.

  **Body (JSON):**
  ```json
  {
    "message": "sua pergunta aqui",
    "history": [
      { "role": "user", "content": "mensagem anterior" },
      { "role": "assistant", "content": "resposta anterior" }
    ]
  }
  ```

  **Resposta (JSON):**
  ```json
  {
    "response": "resposta do chatbot"
  }
  ```

---

## Estrutura básica do projeto

- `app.py` – API FastAPI e endpoints.
- `rag_engine.py` – motor RAG (integração com LangGraph/LangChain).
- `knowledge_base.py` – carregamento e tratamento da base de conhecimento.
- `templates/` – HTML do front-end.
- `static/` – arquivos estáticos (CSS, JS, etc.).
- `requirements.txt` – dependências Python.
- `Dockerfile` – definição da imagem Docker.
- `docker-compose.yml` – orquestração com Docker Compose.
