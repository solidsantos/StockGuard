# StockGuard 1.0 — API de Controle de Estoque

## 1. Descrição

O StockGuard 1.0 é uma API REST desenvolvida em Python com FastAPI para gerenciamento de produtos, movimentações de estoque, monitoramento de estoque mínimo e geração de alertas de reposição.

O projeto também disponibiliza um assistente de ajuda com Inteligência Artificial, utilizando recuperação de informações de 20 políticas operacionais em Markdown e integração HTTP com um provedor de IA online.

## 2. Tecnologias utilizadas

- Python 3.13
- FastAPI e Uvicorn
- Pydantic
- SQLite
- HTTPX
- Pytest
- Python-dotenv
- Groq API (interface compatível com OpenAI)

## 3. Funcionalidades

- Cadastro de produtos com SKU único.
- Listagem e consulta individual de produtos.
- Atualização de dados cadastrais sem alteração direta do saldo.
- Movimentações de entrada (IN), saída (OUT) e ajuste (ADJUST).
- Histórico de movimentações.
- Validação de estoque insuficiente.
- Abertura e resolução de alertas de estoque mínimo.
- Varredura idempotente de alertas.
- Consulta e filtragem de alertas.
- Assistente de ajuda baseado em políticas operacionais e IA online.

## 4. Instalação e configuração

### 4.1. Criar o ambiente virtual

No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4.2. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4.3. Configurar as variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Para utilizar a integração com a Groq, configure no `.env`:

```dotenv
STOCKGUARD_DB=stockguard.sqlite3
AI_MODE=openai_compatible
AI_BASE_URL=https://api.groq.com/openai/v1
AI_API_KEY=SUA_CHAVE_AQUI
AI_MODEL=openai/gpt-oss-20b
AI_TIMEOUT=20
```

A chave de API deve ser obtida no provedor escolhido.

**Nunca compartilhe o arquivo `.env` ou uma chave de API real.**

## 5. Executar a aplicação

Com o ambiente virtual ativado, execute:

```powershell
python -m uvicorn app.main:app --reload
```

A documentação interativa da API estará disponível em:

http://127.0.0.1:8000/docs

A documentação alternativa estará disponível em:

http://127.0.0.1:8000/redoc

O banco de dados SQLite será inicializado automaticamente na inicialização da aplicação.

## 6. Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/items` | Cadastrar produto |
| GET | `/items` | Listar produtos |
| GET | `/items/{item_id}` | Consultar produto |
| PATCH | `/items/{item_id}` | Atualizar dados cadastrais |
| POST | `/items/{item_id}/movements` | Registrar movimentação |
| GET | `/items/{item_id}/movements` | Consultar histórico |
| POST | `/automation/check` | Executar varredura de alertas |
| GET | `/alerts` | Consultar alertas |
| POST | `/help` | Consultar assistente com IA |

### 6.1. Movimentações de estoque

O sistema oferece três operações:

- **IN:** adiciona uma quantidade positiva ao estoque.
- **OUT:** retira uma quantidade positiva, desde que exista saldo suficiente.
- **ADJUST:** define o saldo absoluto do produto, sem permitir valores negativos.

As movimentações são registradas em transações SQLite, preservando a consistência entre o saldo e o histórico.

O saldo não pode ser modificado diretamente pelo endpoint PATCH.

### 6.2. Automação de alertas

A rota `POST /automation/check` verifica os produtos cadastrados.

Quando o estoque é menor ou igual ao mínimo configurado, o sistema abre um alerta caso não exista outro aberto para o mesmo produto.

Quando o estoque supera o mínimo, um alerta aberto é resolvido.

A varredura é idempotente: executá-la repetidamente sem alterações de estoque não cria alertas duplicados.

Os alertas podem ser consultados em `/alerts`, com filtragem opcional por `alert_status=OPEN` ou `alert_status=RESOLVED`.

### 6.3. Assistente com Inteligência Artificial

O endpoint `POST /help` recebe uma pergunta e recupera documentos relevantes do diretório `knowledge/`.

A recuperação utiliza busca lexical sobre 20 políticas operacionais em Markdown.

Quando encontra documentos relevantes, o serviço envia a pergunta e o contexto documental para um provedor de IA online configurado por variáveis de ambiente.

A resposta inclui o texto gerado, as fontes recuperadas, o provedor e o modelo utilizado.

O assistente não executa movimentações, não altera produtos e não consulta diretamente os saldos operacionais.

Quando não encontra documentação relevante, retorna uma mensagem informativa sem consultar o provedor externo.

## 7. Testes automatizados

Os testes utilizam Pytest e o TestClient do FastAPI.

Para executar:

```powershell
python -m pytest tests/ -v
```

Para obter um resumo:

```powershell
python -m pytest tests/ -q
```

Na última execução de validação, foram aprovados **26 testes automatizados**, cobrindo:

- Cadastro e consulta de produtos.
- Validação de dados e SKU duplicado.
- Atualização cadastral.
- Movimentações e proteção contra saldo negativo.
- Atomicidade em movimentações rejeitadas.
- Automação e idempotência dos alertas.
- Resolução e filtragem de alertas.
- Integração simulada com IA.
- Tratamento de falhas do provedor de IA.

Os testes utilizam um banco SQLite temporário e simulam as requisições HTTP externas à IA, evitando consumo de créditos ou dependência de conexão com o provedor.

A integração real com a Groq também foi verificada manualmente durante o desenvolvimento.

## 8. Estrutura do projeto

```text
app/
    __init__.py
    main.py
    db.py
    schemas.py
    policy_search.py
    help_service.py

knowledge/
    manifest.json
    20 arquivos Markdown de políticas

tests/
    conftest.py
    test_stockguard.py

.env.example
.gitignore
README.md
requirements.txt
requests.http
```

## 9. Segurança e limitações

- As credenciais são configuradas exclusivamente por variáveis de ambiente.
- O arquivo `.env` não deve ser distribuído.
- O banco SQLite é utilizado para persistência local.
- O assistente de IA depende da disponibilidade do provedor externo quando existem documentos relevantes.
- As respostas da IA são baseadas nas políticas recuperadas, mas devem ser verificadas pelo operador.
- A API foi desenvolvida para fins acadêmicos e não inclui autenticação de usuários.

## 10. Evidências e entrega

A entrega do projeto deve incluir:

- Código-fonte da API.
- Políticas operacionais.
- Arquivos de configuração de exemplo.
- Documentação de instalação e execução.
- Testes automatizados.
- Evidências de funcionamento no Swagger e dos testes.

Não devem ser incluídos o ambiente virtual, credenciais reais, caches ou bancos de desenvolvimento.