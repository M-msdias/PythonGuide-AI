# Avaliação de Prompt Engineering

## Objetivo

Comparar o comportamento do chatbot antes e depois das melhorias de Prompt Engineering, incluindo as variantes Zero-Shot e Few-Shot.

A avaliação também verifica o comportamento do sistema diante de situações de ausência de evidência e de tentativas de Prompt Injection.

Os testes avaliam:

- resposta para perguntas dentro do domínio;
- comportamento para perguntas fora do domínio;
- diferença entre Zero-Shot e Few-Shot;
- resistência a Prompt Injection direto;
- resistência a Indirect Prompt Injection;
- utilização do contexto recuperado;
- comportamento quando não há evidência suficiente.

---

## Estratégia de Prompt Engineering

A atividade manteve a mesma base de conhecimento, embeddings, índice vetorial, fluxo de recuperação e interface web da atividade anterior.

As mudanças foram concentradas na construção, organização e avaliação dos prompts enviados ao LLM.

### Prompt utilizado antes das melhorias

Na versão inicial, o prompt reunia contexto recuperado, histórico e pergunta do usuário em uma única instrução, sem deixar tão explícita a diferença entre:

- instruções que definem o comportamento do modelo;
- dados recuperados pela busca;
- histórico da conversa;
- pergunta atual do usuário.

Também não havia uma política tão explícita para determinar o comportamento quando a recuperação não fornecia evidência suficiente.

A avaliação baseline dessa versão está registrada em:

`docs/prompt-evaluation-before.md`

### Prompt após as melhorias

O prompt passou a utilizar duas camadas:

1. **System message:** contém as instruções permanentes que definem o comportamento do PythonGuide AI.
2. **Human message:** contém os dados específicos daquela interação, incluindo evidência recuperada, histórico e pergunta do usuário.

Essa separação permite distinguir as instruções de comportamento dos dados utilizados para gerar a resposta.

---

## Instruções de sistema

O System Prompt define, entre outros pontos:

- o papel do modelo como assistente especializado em Python;
- resposta em português do Brasil;
- utilização prioritária das evidências recuperadas;
- proibição de inventar informações não sustentadas pelo contexto;
- comportamento específico quando não existe evidência suficiente;
- tratamento do conteúdo recuperado como dados, e não como instruções;
- tratamento do histórico como contexto, e não como instruções;
- utilização de Markdown e blocos de código quando apropriado;
- comportamento didático e objetivo;
- prioridade das instruções do sistema sobre conteúdo presente no contexto recuperado ou no histórico.

---

## Separação entre instruções e dados

Os dados da interação são delimitados explicitamente no Human Prompt:

```text
<EVIDENCIA_DISPONIVEL>
{evidence_status}
</EVIDENCIA_DISPONIVEL>

<CONTEXTO_RECUPERADO>
{context}
</CONTEXTO_RECUPERADO>

<HISTORICO_DA_CONVERSA>
{history}
</HISTORICO_DA_CONVERSA>

<PERGUNTA_DO_USUARIO>
{question}
</PERGUNTA_DO_USUARIO>