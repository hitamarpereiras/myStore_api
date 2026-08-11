<div align="center">

# My Store API

<p>API REST para gerenciamento de lojas, produtos, categorias, pedidos e contas da plataforma <strong>My Store</strong>.</p>

![Python](https://img.shields.io/badge/Python-3.12%2B-1f3a5f?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-1f3a5f?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-4b5563?style=flat-square)
![JWT](https://img.shields.io/badge/Auth-JWT-334155?style=flat-square)
![Database](https://img.shields.io/badge/Database-PostgreSQL-475569?style=flat-square&logo=postgresql&logoColor=white)

</div>

## Visão geral

O projeto oferece autenticação JWT, administração pelo Django Admin e recursos para contas, lojas, categorias, produtos e pedidos. Lojas e produtos aceitam imagens, que são processadas e armazenadas no Supabase Storage.

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

A API estará disponível na URL configurada para o ambiente. Nos exemplos abaixo, substitua `{{BASE_URL}}` pela URL da sua API, por exemplo `https://api.exemplo.com`.

## Autenticação JWT

### Obter tokens

Envie o e-mail e a senha de um usuário existente:

```bash
curl -X POST {{BASE_URL}}/api/v1/authentication/token/ \
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
curl {{BASE_URL}}/api/v1/categories/ \
  -H "Authorization: Bearer <access_token>"
```

O access token expira em 15 dias. O refresh token expira em 20 dias; ao renová-lo, um novo refresh token é emitido e o anterior é invalidado.

```bash
curl -X POST {{BASE_URL}}/api/v1/authentication/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

## Rotas da API

Base URL: `{{BASE_URL}}`

| Recurso | Rota | Acesso | Métodos |
| --- | --- | --- | --- |
| Tokens JWT | `/api/v1/authentication/token/` | Público | `POST` |
| Renovação JWT | `/api/v1/authentication/token/refresh/` | Público | `POST` |
| Contas | `/api/v1/accounts/` e `/api/v1/accounts/{id}/` | JWT | `GET`, `PATCH` |
| Cadastro de contas | `/api/v1/accounts/register/` | Administrador JWT | `POST` |
| Lojas | `/api/v1/stores/` e `/api/v1/stores/{id}/` | Leitura pública; escrita JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Categorias | `/api/v1/categories/` e `/api/v1/categories/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Produtos | `/api/v1/products/` e `/api/v1/products/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Vendas | `/api/v1/sales/` e `/api/v1/sales/{id}/` | JWT + `X-Store-ID` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Pedidos | `/api/v1/orders/` e `/api/v1/orders/{id}/` | JWT | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Confirmar entrega | `/api/v1/orders/{id}/confirm-delivery` | JWT | `POST` |
| Administração | `/adm/` | Sessão de administrador | Interface Django Admin |

As listagens são paginadas. Para contas, lojas e categorias, o padrão é 40 itens por página, com `?page=` e `?page_size=` (máximo de 80). Produtos utilizam 14 itens por página e aceitam `page_size` de até 28.

### Contas

`GET /api/v1/accounts/` e `GET /api/v1/accounts/{id}/` exigem JWT. Usuários comuns consultam apenas a própria conta; superusuários podem consultar todas. As únicas operações permitidas nesse recurso são `GET` e `PATCH` — não há `POST`, `PUT` nem `DELETE`.

O retorno contém `email`, `username`, `first_name`, `last_name` e `telephone`; a senha nunca é exposta. É possível atualizar parcialmente esses campos com `PATCH`, mas não alterar a senha por essa rota.

O cadastro é feito em `POST /api/v1/accounts/register/` e exige um token de superusuário. Envie `email`, `username` e `password`; `first_name`, `last_name` e `telephone` são opcionais.

```bash
curl -X POST {{BASE_URL}}/api/v1/accounts/register/ \
  -H "Authorization: Bearer <admin_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nova-conta@example.com",
    "username": "nova_conta",
    "password": "uma-senha-segura"
  }'
```

### Lojas

`GET /api/v1/stores/` e `GET /api/v1/stores/{id}/` são públicos. Criação, alteração e exclusão exigem JWT e só alcançam lojas pertencentes ao usuário autenticado.

Os filtros aceitos na listagem são `id`, `owner` e `cnpj`:

```text
GET /api/v1/stores/?cnpj=12.345.678/0001-90
```

Para criar uma loja, envie `multipart/form-data` com o campo `image`. O arquivo deve ser uma imagem válida de até 1 MB; ele é convertido para JPEG, redimensionado e armazenado no bucket `avatar_lojas`.

| Campo | Tipo | Observação |
| --- | --- | --- |
| `name` | texto | Obrigatório |
| `phone`, `address`, `cnpj` | texto | Opcionais |
| `instagram_url`, `facebook_url`, `other_url` | URL | Opcionais |
| `image` | arquivo | Enviar como multipart; até 1 MB |
| `owner` | — | Definido automaticamente pelo token |
| `avatar_url`, `color_palette`, `created_at`, `updated_at` | — | Gerados pela API e somente leitura |

Exemplo:

```bash
curl -X POST {{BASE_URL}}/api/v1/stores/ \
  -H "Authorization: Bearer <access_token>" \
  -F "name=Minha Loja" \
  -F "cnpj=12.345.678/0001-90" \
  -F "image=@./avatar.png"
```

As operações de criação e atualização retornam a representação da loja. A exclusão retorna `204 No Content`. Na troca ou exclusão, a API tenta remover o avatar anterior do Supabase.

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

A listagem aceita os filtros `category`, `price`, `name` e `store`. Para carregar os produtos de uma loja específica, o front-end deve enviar o ID da loja no parâmetro `store`:

```text
GET /api/v1/products/?store=abc123
```

O filtro `store` também pode ser combinado com paginação e os demais filtros, por exemplo: `GET /api/v1/products/?store=abc123&category=2&page=1&page_size=14`. Usuários comuns recebem somente produtos das próprias lojas; superusuários podem consultar produtos de qualquer loja.

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
curl -X POST {{BASE_URL}}/api/v1/products/ \
  -H "Authorization: Bearer <access_token>" \
  -F "store=ABC123" \
  -F "name=Fone Bluetooth" \
  -F "category=2" \
  -F "price=199.90" \
  -F "stock=10" \
  -F "image=@./fone.png"
```

Ao criar, atualizar ou excluir um produto, a API retorna uma mensagem de confirmação. Na troca ou exclusão, ela tenta remover a imagem anterior do Supabase.

### Vendas

Todos os endpoints de vendas exigem JWT e o header `X-Store-ID`. O front-end deve enviar nele o ID da loja que está sendo utilizada no momento. Esse header é obrigatório também para consultar, atualizar ou excluir uma venda individual.

```text
X-Store-ID: ABC123
```

A API valida que a loja indicada pertence ao usuário autenticado. Portanto, não envie `store` nem `account` no corpo da requisição: ambos são definidos pelo backend a partir do header e do token JWT. As listagens retornam somente vendas da loja selecionada e do usuário autenticado.

| Campo | Tipo | Observação |
| --- | --- | --- |
| `order` | ID do pedido | Obrigatório; um pedido pode estar vinculado a somente uma venda |
| `total`, `subtotal`, `remaining`, `rate_delivery` | decimal | Opcionais; padrão `0.00` |
| `payment_method` | texto | Opcional; máximo de 15 caracteres |
| `collaborator` | texto | Opcional; máximo de 50 caracteres |
| `observation` | texto | Opcional; máximo de 200 caracteres |
| `status` | booleano | Opcional; padrão `false` |
| `account`, `store`, `created_at`, `updated_at` | — | Definidos pela API; não enviar no payload |

Exemplo de criação:

```bash
curl -X POST {{BASE_URL}}/api/v1/sales/ \
  -H "Authorization: Bearer <access_token>" \
  -H "X-Store-ID: ABC123" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 42,
    "subtotal": "90.00",
    "rate_delivery": "10.00",
    "total": "100.00",
    "payment_method": "pix",
    "collaborator": "Maria"
  }'
```

Para listar ou acessar uma venda, mantenha os dois headers:

```bash
curl {{BASE_URL}}/api/v1/sales/ \
  -H "Authorization: Bearer <access_token>" \
  -H "X-Store-ID: ABC123"
```

Se `X-Store-ID` não for enviado, a API retorna `403 Forbidden` informando que o header é obrigatório. O mesmo status é retornado quando a loja não pertence ao usuário autenticado. Uma venda que não pertença à loja selecionada não é exposta pela API.

### Pedidos

Todos os endpoints de pedidos exigem JWT. A listagem retorna os pedidos da loja associada ao usuário autenticado; clientes visualizam apenas os próprios pedidos. Os filtros disponíveis são `created_at`, `code` e `total`:

```text
GET /api/v1/orders/?code=12345
GET /api/v1/orders/?total=49.90
```

| Campo | Tipo | Observação |
| --- | --- | --- |
| `customer` | ID da conta | Cliente vinculado ao pedido |
| `name_customer`, `phone` | texto | Obrigatórios |
| `address` | texto | Obrigatório |
| `house_number`, `observation` | texto | Opcionais |
| `latitude`, `longitude` | decimal | Opcionais; localização de entrega |
| `subtotal`, `rate_delivery`, `total`, `remaining` | decimal | Valores monetários do pedido e troco |
| `payment_method` | texto | Opcional |
| `itens` | JSON | Obrigatório; lista de produtos do pedido, cada um com `id`, `name`, `price` e `quantity` |
| `status` | texto | Somente leitura; `pendente`, `entregue` ou `cancelado`; padrão `pendente` |
| `code` | texto | Código de entrega de 4 caracteres, gerado para o pedido |
| `created_at` | data e hora | Gerado pela API; somente leitura |

O campo `itens` deve ser enviado como uma lista JSON. Exemplo:

```json
[
  {
    "id": 5,
    "name": "Mouse",
    "price": 19.00,
    "quantity": 2
  }
]
```

#### Confirmação de entrega

A confirmação exige JWT e valida um código de entrega de quatro caracteres enviado no corpo da requisição:

```bash
curl -X POST {{BASE_URL}}/api/v1/orders/{id}/confirm-delivery \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"code": "a1b2"}'
```

Quando a confirmação é aceita, a API retorna `200 OK`:

```json
{
  "detail": "Entrega confirmada com sucesso."
}
```

Substitua `{id}` pelo identificador do pedido. O código é obrigatório e deve conter exatamente quatro caracteres. A confirmação é permitida somente para o entregador vinculado ao pedido e para pedidos pendentes; código inválido, pedido já processado ou falta de permissão retornam erro.

## Postman

Há uma coleção pronta em [postman/My_Store_API.postman_collection.json](postman/My_Store_API.postman_collection.json). Importe-a no Postman, preencha as variáveis `email` e `password` e execute o login para armazenar automaticamente os tokens. Antes de criar ou atualizar uma loja com imagem, selecione um arquivo local no campo `image`.

## Administração

Com o servidor em execução, acesse `{{BASE_URL}}/adm/` usando o superusuário criado anteriormente.

---

<div align="center">
  <sub>My Store API · Django REST Framework</sub>
</div>
