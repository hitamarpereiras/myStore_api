<div align="center">

# My Store API

<p>API REST para gerenciamento de lojas, produtos, categorias e contas da plataforma <strong>My Store</strong>.</p>

![Python](https://img.shields.io/badge/Python-3.12%2B-1f3a5f?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-1f3a5f?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-4b5563?style=flat-square)
![JWT](https://img.shields.io/badge/Auth-JWT-334155?style=flat-square)
![Database](https://img.shields.io/badge/Database-PostgreSQL-475569?style=flat-square&logo=postgresql&logoColor=white)

</div>

## Visão geral

O projeto oferece autenticação JWT, administração pelo Django Admin e recursos para contas, lojas, categorias e produtos. Lojas e produtos aceitam imagens, que são processadas e armazenadas no Supabase Storage.

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.12+ |
| Framework | Django 6 |
| API | Django REST Framework |
| Autenticação | Simple JWT |
| Banco de dados | PostgreSQL |
| Arquivos | Supabase Storage |
| Configuração | Pydantic Settings + `.env` |

## Início rápido

### Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL acessível pela aplicação
- Projeto e bucket `avatar_lojas` configurados no Supabase
- `pip`

### 1. Clone o repositório e entre na pasta

```bash
git clone <URL_DO_REPOSITORIO>
cd mystore_api
```

### 2. Crie e ative o ambiente virtual

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

Crie o arquivo `.env` na raiz. Não versione chaves, credenciais nem URLs reais.

```env
APP_NAME=my store
DATABASE_URL=postgresql://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=SUA_CHAVE_DO_SUPABASE
```

`DATABASE_URL`, `SUPABASE_URL` e `SUPABASE_KEY` são obrigatórias para a inicialização atual. A aplicação exige conexão SSL com o PostgreSQL. O `DEBUG` está definido diretamente nas configurações do Django.

### 5. Aplique as migrações e crie um administrador

```bash
python manage.py migrate
python manage.py createsuperuser
```

O usuário personalizado utiliza o **e-mail** para autenticação; informe também um `username` ao criar o superusuário.

### 6. Inicie o servidor

```bash
python manage.py runserver
```

A API local estará disponível em `http://127.0.0.1:8000/`, e o painel administrativo em `http://127.0.0.1:8000/adm/`.

## Autenticação JWT

### Obter tokens

Envie o e-mail e a senha de um usuário existente:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu_email@example.com",
    "password": "sua_senha"
  }'
```

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Use o token de acesso nas rotas protegidas:

```bash
curl http://127.0.0.1:8000/api/v1/categories/ \
  -H "Authorization: Bearer <access_token>"
```

O access token expira em 15 dias. O refresh token expira em 20 dias; ao renová-lo, um novo refresh token é emitido e o anterior é invalidado.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authentication/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

## Rotas da API

Base URL local: `http://127.0.0.1:8000`

| Recurso | Rota | Acesso | Métodos |
| --- | --- | --- | --- |
| Tokens JWT | `/api/v1/authentication/token/` | Público | `POST` |
| Renovação JWT | `/api/v1/authentication/token/refresh/` | Público | `POST` |
| Contas | `/api/v1/accounts/` e `/api/v1/accounts/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Lojas | `/api/v1/stores/` e `/api/v1/stores/{id}/` | Leitura pública; escrita JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Categorias | `/api/v1/categories/` e `/api/v1/categories/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Produtos | `/api/v1/products/` e `/api/v1/products/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Administração | `/adm/` | Sessão de administrador | Interface Django Admin |

As listagens são paginadas. Para contas, lojas e categorias, o padrão é 40 itens por página, com `?page=` e `?page_size=` (máximo de 80). Produtos utilizam 14 itens por página e aceitam `page_size` de até 28.

### Contas

O retorno de uma conta contém `id`, `email`, `first_name`, `last_name`, `is_active` e `telephone`; a senha não é exposta pelo serializer. Usuários comuns consultam apenas a própria conta, enquanto superusuários podem consultar todas. Para definir ou alterar senhas, use o Django Admin.

### Lojas

`GET /api/v1/stores/` e `GET /api/v1/stores/{id}/` são públicos. Criação, alteração e exclusão exigem JWT e só alcançam lojas pertencentes ao usuário autenticado.

Os filtros aceitos na listagem são `id`, `owner` e `cnpj`:

```text
GET /api/v1/stores/?cnpj=12.345.678/0001-90
```

Para criar uma loja, envie `multipart/form-data`. No estado atual da API, o campo `image` deve ser enviado na criação. O arquivo deve ser uma imagem válida de até 1 MB; ele é convertido para JPEG, redimensionado e armazenado no bucket `avatar_lojas`.

| Campo | Tipo | Observação |
| --- | --- | --- |
| `name` | texto | Obrigatório |
| `slog` | texto | Opcional; máximo de 150 caracteres |
| `phone`, `address`, `cnpj` | texto | Opcionais |
| `instagram_url`, `facebook_url`, `other_url` | URL | Opcionais |
| `image` | arquivo | Enviar como multipart; até 1 MB |
| `owner` | — | Definido automaticamente pelo token |
| `avatar_url`, `color_palette` | — | Gerados pela API e somente leitura |

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/stores/ \
  -H "Authorization: Bearer <access_token>" \
  -F "name=Minha Loja" \
  -F "slog=Tudo para sua casa" \
  -F "cnpj=12.345.678/0001-90" \
  -F "image=@./avatar.png"
```

Ao criar, atualizar ou excluir uma loja, a API retorna uma mensagem de confirmação. Na troca ou exclusão, ela tenta remover o avatar anterior do Supabase.

### Categorias

Categorias sempre exigem JWT. O proprietário é preenchido automaticamente na criação e não pode ser informado pelo cliente. Usuários comuns acessam apenas as próprias categorias; superusuários acessam todas.

Filtros disponíveis: `name`, `owner` e `store`.

```json
{
  "store": "ABC123",
  "name": "Eletrônicos",
  "description": "Produtos eletrônicos"
}
```

`store` é opcional e referencia o ID de uma loja. O nome da categoria é único em toda a base de dados.

### Produtos

Todos os endpoints de produtos exigem JWT. Usuários comuns visualizam e administram somente produtos dos quais são proprietários; superusuários podem visualizar todos os produtos.

A listagem aceita os filtros `category`, `price` e `name`. Usuários comuns também podem restringir o resultado à loja com o parâmetro `store`:

```text
GET /api/v1/products/?store=ABC123&category=2&page=1&page_size=14
```

Na criação, envie `multipart/form-data` e inclua a imagem do produto. O arquivo deve ser uma imagem válida de até 1 MB; a API o converte para JPEG de 1024 × 1024 px e o armazena no bucket `products` do Supabase.

| Campo | Tipo | Observação |
| --- | --- | --- |
| `store` | ID da loja | Obrigatório |
| `name` | texto | Obrigatório; máximo de 100 caracteres |
| `category` | lista de IDs | Obrigatório; uma ou mais categorias |
| `description` | texto | Opcional; máximo de 320 caracteres |
| `price` | decimal | Opcional; padrão `0.00` |
| `stock` | inteiro | Opcional; padrão `0` |
| `image` | arquivo | Enviar como multipart; até 1 MB |
| `crop_x`, `crop_y`, `crop_width`, `crop_height` | inteiro | Opcionais; metadados de recorte para o front-end |
| `owner` | — | Definido automaticamente pelo token |
| `image_url`, `image_path` | — | Gerados pela API e somente leitura |

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/products/ \
  -H "Authorization: Bearer <access_token>" \
  -F "store=ABC123" \
  -F "name=Fone Bluetooth" \
  -F "category=2" \
  -F "price=199.90" \
  -F "stock=10" \
  -F "image=@./fone.png"
```

Ao criar, atualizar ou excluir um produto, a API retorna uma mensagem de confirmação. Na troca ou exclusão, ela tenta remover a imagem anterior do Supabase.

## Postman

Há uma coleção pronta em [postman/My_Store_API.postman_collection.json](postman/My_Store_API.postman_collection.json). Importe-a no Postman, preencha as variáveis `email` e `password` e execute o login para armazenar automaticamente os tokens. Antes de criar ou atualizar uma loja com imagem, selecione um arquivo local no campo `image`.

## Administração

Com o servidor em execução, acesse [http://127.0.0.1:8000/adm/](http://127.0.0.1:8000/adm/) usando o superusuário criado anteriormente.

---

<div align="center">
  <sub>My Store API · Django REST Framework</sub>
</div>
