# News API

API REST para uma newsletter personalizada. Usuários se cadastram, definem interesses e recebem um feed de notícias filtrado por categoria.

## Funcionalidades

**Disponível hoje (camada de serviço)**

- Validação de e-mail
- Registro e login com JWT
- Refresh token com rotação e expiração no MongoDB

**Em desenvolvimento**

- Ingestão de notícias via NewsAPI
- Feed diário paginado por interesses

## Stack

| Tecnologia | Uso |
|------------|-----|
| Python 3.14+ | runtime |
| FastAPI | API HTTP |
| Motor | MongoDB async |
| PyJWT + bcrypt | autenticação |
| Pydantic Settings | configuração via `.env` |

## Arquitetura

```
HTTP Request
    ↓
Router          validação de entrada/saída (Pydantic)
    ↓
Service         regras de negócio
    ↓
Repository      persistência (MongoDB)
```

```
newsAPIgithub/
├── config/           settings e variáveis de ambiente
├── core/             hash de senha e JWT
├── database/         conexão e índices do MongoDB
├── model/            contratos de dados (request/response)
├── repositories/     queries nas coleções
├── services/         lógica de aplicação
└── main.py           entrypoint FastAPI
```

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/)
- MongoDB em execução
- Chave da [NewsData.io](https://newsdata.io) *(necessária nas próximas etapas)*

## Executar

```bash
uv sync
uv run python main.py
```

| URL | Descrição |
|-----|-----------|
| http://localhost:8000 | raiz |
| http://localhost:8000/health | status da API |
| http://localhost:8000/docs | documentação interativa |

## Endpoints planejados

### Auth

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/validate` | verifica se o e-mail já está cadastrado |
| POST | `/api/register` | cria conta e retorna tokens |
| POST | `/api/login` | autentica e retorna tokens |
| POST | `/api/refresh` | renova o access token |

### Usuário

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/user/me` | perfil do usuário logado |
| PUT | `/api/interests` | categorias e filtros do feed |
| PUT | `/api/user/preferences` | preferências (ex.: dark mode) |

### Notícias

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/news/daily` | feed do dia (paginado) |
| GET | `/api/news/{id}` | detalhe da notícia |
| POST | `/api/admin/ingest-news` | ingestão manual de notícias |

## Coleções MongoDB

| Coleção | Conteúdo |
|---------|----------|
| `users` | conta, senha hasheada, interesses e preferências |
| `refresh_tokens` | tokens de renovação com TTL automático |
| `news` | notícias ingeridas *(em breve)* |

## Roadmap

- [x] Models, config e conexão com MongoDB
- [x] Segurança (bcrypt + JWT)
- [x] Repositories e `AuthService`
- [x] Routers e injeção de dependência
- [x] Endpoints de usuário
- [x] Ingestão e feed de notícias

## Licença

[MIT](LICENSE)
