<div align="center">

# My Store API

<p>API REST para a plataforma <strong>My Store</strong>, desenvolvida com Django.</p>

![Python](https://img.shields.io/badge/Python-3.12%2B-1f3a5f?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-1f3a5f?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-4b5563?style=flat-square)
![JWT](https://img.shields.io/badge/Auth-JWT-334155?style=flat-square)
![Database](https://img.shields.io/badge/Database-PostgreSQL-475569?style=flat-square&logo=postgresql&logoColor=white)

</div>

<br>

<table>
  <tr>
    <td width="33%" align="center">
      <strong>API REST</strong><br>
      Endpoints versionados em <code>/api/v1/</code>
    </td>
    <td width="33%" align="center">
      <strong>Autenticação</strong><br>
      Tokens de acesso e renovação com JWT
    </td>
    <td width="33%" align="center">
      <strong>Administração</strong><br>
      Painel administrativo nativo do Django
    </td>
  </tr>
</table>

## Visão geral

O projeto disponibiliza a base de uma API para gerenciamento da My Store. Atualmente, inclui autenticação por JSON Web Token (JWT), administração pelo Django Admin e um recurso protegido para contas.

### Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.12+ |
| Framework | Django 6 |
| API | Django REST Framework |
| Autenticação | Simple JWT |
| Banco de dados | PostgreSQL |
| Configuração | Pydantic Settings + `.env` |

## Início rápido

### Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL acessível pela aplicação
- `pip`

### 1. Clone o repositório e entre na pasta

```bash
git clone <URL_DO_REPOSITORIO>
cd mystore_api
```

### 2. Crie e ative o ambiente virtual

<table>
  <tr>
    <th>Sistema</th>
    <th>Comando</th>
  </tr>
  <tr>
    <td>Windows (PowerShell)</td>
    <td><code>python -m venv venv; .\venv\Scripts\Activate.ps1</code></td>
  </tr>
  <tr>
    <td>Linux / macOS</td>
    <td><code>python3 -m venv venv &amp;&amp; source venv/bin/activate</code></td>
  </tr>
</table>

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

Crie um arquivo `.env` na raiz do projeto. Não versione credenciais ou URLs reais.

```env
APP_NAME=my store
DEBUG=true
DATABASE_URL=postgresql://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO
```

> `DEBUG` aceita somente valores booleanos, como `true` ou `false`.

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

## Rotas da API

Base URL local: `http://127.0.0.1:8000`

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| `POST` | `/api/v1/authentication/token/` | Não | Obtém tokens JWT de acesso e renovação. |
| `POST` | `/api/v1/authentication/token/refresh/` | Não | Renova o token de acesso a partir de um refresh token. |
| `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | `/api/v1/accounts/` | Bearer JWT | Recurso de contas, exposto pelo router do Django REST Framework. |
| — | `/` | Sessão do Django Admin | Painel administrativo do Django. |

> As rotas de contas são protegidas e exigem um usuário autenticado no banco de dados.

## Autenticação JWT

### Obter tokens

Envie as credenciais do usuário para criar os tokens. O campo de identificação depende do modelo de usuário ativo na aplicação; na configuração padrão do Django, use `username`.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

Resposta esperada:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Usar o token de acesso

```bash
curl http://127.0.0.1:8000/api/v1/accounts/ \
  -H "Authorization: Bearer <access_token>"
```

### Renovar o token de acesso

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

## Administração

Com o servidor em execução, acesse o Django Admin em [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Para criar um administrador, execute:

```bash
python manage.py createsuperuser
```

## Estado atual e observações técnicas

- O valor `DEBUG=release` não é válido na configuração atual e impede a inicialização da aplicação. Defina `DEBUG=true` para desenvolvimento ou `DEBUG=false` para produção.
- No estado atual, `manage.py check` também identifica conflito entre `accounts.User` e o usuário padrão do Django. A aplicação precisa definir o modelo de usuário customizado corretamente antes de executar migrações ou disponibilizar as rotas de contas em um ambiente novo.
- O recurso `/api/v1/accounts/` requer autenticação JWT e usuários previamente configurados no banco.
- A conexão com o PostgreSQL é obtida pela variável `DATABASE_URL`; mantenha essa informação fora do controle de versão.

---

<div align="center">
  <sub>My Store API · Django REST Framework</sub>
</div>
