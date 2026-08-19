# 🛍️ My Store API

> API REST para operar uma plataforma de lojas: contas, clientes, catálogo, pedidos e vendas.

![Django](https://img.shields.io/badge/Django-6.0-0C4B33?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-A30000?style=for-the-badge)
![JWT](https://img.shields.io/badge/Autenticação-JWT-6B4EFF?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Banco-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

---

## ✨ Visão geral

A **My Store API** é um backend Django REST Framework com autenticação JWT. Ela separa a operação por lojas e permite que clientes consultem o catálogo e façam pedidos, enquanto os responsáveis pela loja administram catálogo e vendas.

| Ambiente               | Endereço                       |
| ---------------------- | ------------------------------- |
| Local                  | `http://localhost:8000`       |
| Produção             | `https://exemploapistore.com` |
| Base da API            | `{BASE_URL}/api/v1/`          |
| Administração Django | `{BASE_URL}/adm/`             |

> 💡 Todos os caminhos documentados abaixo já começam em `/api/v1`.

## 🎨 Apps do projeto

| App                        | Papel no sistema                                                 |
| -------------------------- | ---------------------------------------------------------------- |
| 🔐**authentication** | Emite e renova tokens JWT.                                       |
| 👤**accounts**       | Gerencia contas de usuários da plataforma e lojistas.           |
| 🧑‍💼**customers**  | Cadastro público e perfil de clientes, avatar e moedas.         |
| 🏪**stores**         | Cadastro, identidade visual e dados das lojas.                   |
| 🗂️**categories**   | Organização do catálogo por categoria.                        |
| 📦**products**       | Produtos, estoque, categorias, imagem e recorte.                 |
| 🧾**orders**         | Pedidos, endereço de entrega, pagamento, itens e confirmação. |
| 💰**sales**          | Registro das vendas associadas a pedidos e à loja ativa.        |

---

## 🚀 Como executar localmente

### 1. Pré-requisitos

- Python 3.12+ recomendado;
- PostgreSQL acessível pela aplicação;
- credenciais de um projeto Supabase (usado para armazenar imagens).

### 2. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Não inclua esse arquivo no Git.

```env
DATABASE_URL=postgresql://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_do_supabase
```

### 4. Preparar o banco e iniciar o servidor

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`.

---

## 🔐 Autenticação e headers

As rotas protegidas usam JWT. Primeiro faça login; em seguida, envie o token de acesso em todas as solicitações autenticadas:

```http
Authorization: Bearer <access_token>
```

Produtos, pedidos e vendas também exigem que a loja atual seja indicada pelo header abaixo:

```http
X-Store-ID: ABC123
```

O identificador de loja possui seis caracteres. Sem o `X-Store-ID`, a API retorna `403 Forbidden` nessas áreas.

### Fluxo sugerido

```text
Criar/obter conta → Login JWT → Criar loja → Criar categoria → Criar produto
                                                ↓
Cliente se cadastra → consulta produtos → cria pedido → confirma entrega → registra venda
```

### Convenções da API

- A maioria dos endpoints do `DefaultRouter` usa barra final: `/products/`.
- Requisições com imagem devem ser `multipart/form-data`.
- Requisições sem arquivo podem ser enviadas em JSON quando o endpoint o aceitar; nos exemplos, usamos JSON para leitura simples e `form-data` para uploads.
- Campos somente leitura são preenchidos pelo servidor. Não é necessário enviá-los.
- Listagens são paginadas por padrão: 40 itens por página, até 80 com `?page_size=80`.
- As respostas de listagem paginada incluem `count`, `next`, `previous` e `results`.

---

## 🔐 Authentication — tokens JWT

### Obter tokens

`POST /api/v1/authentication/token/` · Público

```json
{
  "email": "admin@local.test",
  "password": "12345678"
}
```

Resposta `200 OK`:

```json
{
  "refresh": "eyJ...",
  "access": "eyJ..."
}
```

O token de acesso vale por **15 dias**. O refresh token vale por **20 dias**.

### Renovar access token

`POST /api/v1/authentication/token/refresh/` · Público

```json
{
  "refresh": "eyJ..."
}
```

Como a rotação de refresh tokens está habilitada, guarde o novo refresh retornado pela API e descarte o anterior.

---

## 👤 Accounts — contas de usuários

### Criar conta de lojista/usuário

`POST /api/v1/accounts/register/` · 🔒 Somente administrador

```json
{
  "email": "lojista@exemplo.com",
  "username": "mercado_central",
  "password": "UmaSenhaSegura123",
  "first_name": "Maria",
  "last_name": "Souza",
  "telephone": "11988888888"
}
```

Resposta `201 Created`:

```json
{
  "id": "AB12CD34EF",
  "email": "lojista@exemplo.com",
  "username": "mercado_central",
  "first_name": "Maria",
  "last_name": "Souza",
  "telephone": "11988888888"
}
```

### Consultar ou atualizar contas

| Método   | Rota                       | Resultado                                                                   |
| --------- | -------------------------- | --------------------------------------------------------------------------- |
| `GET`   | `/api/v1/accounts/`      | Administrador vê todas as contas; demais usuários veem apenas a própria. |
| `GET`   | `/api/v1/accounts/{id}/` | Retorna uma conta acessível ao usuário.                                   |
| `PATCH` | `/api/v1/accounts/{id}/` | Atualiza parcialmente os campos expostos da conta.                          |

> ℹ️ Este recurso não expõe `POST`, `PUT` ou `DELETE`. O cadastro é feito pela rota `accounts/register/`.

---

## 🧑‍💼 Customers — clientes

### Cadastro público de cliente

`POST /api/v1/customers/register/` · Público · `multipart/form-data`

| Campo            | Obrigatório | Descrição              |
| ---------------- | ------------ | ------------------------ |
| `email`        | Sim          | E-mail único de acesso. |
| `password`     | Sim          | Senha da nova conta.     |
| `first_name`   | Sim          | Primeiro nome.           |
| `last_name`    | Sim          | Sobrenome.               |
| `telephone`    | Não         | Telefone do cliente.     |
| `address`      | Não         | Endereço padrão.       |
| `house_number` | Não         | Número/complemento.     |
| `coins`        | Não         | Saldo inicial de moedas. |
| `image`        | Não         | Avatar do cliente.       |

Exemplo em `form-data`:

```text
email=joao@exemplo.com
password=UmaSenhaSegura123
first_name=João
last_name=Silva
telephone=11999999999
address=Rua das Flores
house_number=123
coins=0
image=@avatar.png
```

Resposta `201 Created`:

```json
{ "message": "Usuário criado com sucesso" }
```

### Perfil e moedas

| Método    | Rota                                  | Descrição                                                                                             |
| ---------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `GET`    | `/api/v1/customers/`                | Lista apenas o perfil de cliente ligado ao usuário autenticado.                                        |
| `GET`    | `/api/v1/customers/{id}/`           | Obtém um perfil do escopo autenticado.                                                                 |
| `PATCH`  | `/api/v1/customers/{id}/`           | Atualiza endereço, número, moedas, premium ou imagem. Use`multipart/form-data` ao enviar `image`. |
| `DELETE` | `/api/v1/customers/{id}/`           | Exclui o perfil e seu avatar armazenado.                                                                |
| `POST`   | `/api/v1/customers/{id}/add-coins/` | Acrescenta moedas ao cliente.                                                                           |

Para adicionar moedas:

```json
{ "coins": 25 }
```

O valor deve ser inteiro e maior que zero. A resposta confirma o novo saldo:

```json
{
  "detail": "Coins adicionadas com sucesso.",
  "coins": 25
}
```

---

## 🏪 Stores — lojas

Uma loja é vinculada automaticamente ao usuário autenticado que a cria. Cada loja recebe um ID de seis caracteres, usado como `X-Store-ID` nas áreas de catálogo, pedidos e vendas.

### Criar loja

`POST /api/v1/stores/` · 🔒 Autenticado · `multipart/form-data`

```text
name=Mercado Local
slog=Perto de você
phone=11999999999
address=Av. Principal, 100
cnpj=12.345.678/0001-90
instagram_url=https://instagram.com/mercadolocal
facebook_url=https://facebook.com/mercadolocal
other_url=https://mercadolocal.com.br
image=@logo.png
```

Ao enviar uma imagem, ela é processada, enviada ao Supabase e também gera uma `color_palette` automaticamente para uso no frontend.

Campos retornados: `id`, `owner`, `name`, `slog`, `phone`, `address`, `cnpj`, `avatar_url`, redes sociais, `color_palette`, `created_at` e `updated_at`.

### Operações disponíveis

| Método    | Rota                     | Descrição                                             |
| ---------- | ------------------------ | ------------------------------------------------------- |
| `GET`    | `/api/v1/stores/`      | Lista as lojas do usuário. Administradores veem todas. |
| `POST`   | `/api/v1/stores/`      | Cria uma loja.                                          |
| `GET`    | `/api/v1/stores/{id}/` | Consulta uma loja.                                      |
| `PATCH`  | `/api/v1/stores/{id}/` | Atualiza dados e/ou logo.                               |
| `DELETE` | `/api/v1/stores/{id}/` | Exclui a loja e remove o avatar associado.              |

Filtros disponíveis: `?id=ABC123`, `?owner=ID_DO_USUARIO` e `?cnpj=...`.

---

## 🗂️ Categories — categorias

As categorias pertencem ao usuário autenticado e podem ser associadas a uma loja. O nome é normalizado para letras minúsculas e deve ser único na base.

### Criar categoria

`POST /api/v1/categories/` · 🔒 Autenticado

```json
{
  "store": "ABC123",
  "name": "Bebidas",
  "description": "Bebidas geladas e não alcoólicas"
}
```

O campo `owner` é preenchido pelo backend; não o envie. A resposta terá `name: "bebidas"`.

### Operações e filtros

| Método                                 | Rota                         |
| --------------------------------------- | ---------------------------- |
| `GET`, `POST`                       | `/api/v1/categories/`      |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/api/v1/categories/{id}/` |

Filtros: `?name=bebidas`, `?owner=ID_DO_USUARIO` e `?store=ABC123`.

---

## 📦 Products — produtos

Todas as rotas deste app precisam de `Authorization` e `X-Store-ID`. Qualquer usuário autenticado pode listar o catálogo da loja selecionada, mas somente o proprietário da loja (ou um administrador) pode criar, editar ou excluir produtos.

### Criar produto

`POST /api/v1/products/` · 🔒 Proprietário/administrador · `multipart/form-data`

```text
X-Store-ID: ABC123

name=Refrigerante Cola 2L
category=1
category=3
description=Refrigerante gelado de dois litros
price=9.90
stock=30
crop_x=0
crop_y=0
crop_width=1024
crop_height=1024
image=@refrigerante.jpg
```

`category` é um relacionamento de múltiplas categorias: envie o campo repetido para associar mais de uma. A imagem é opcional; quando enviada, é processada em até 1024×1024 e armazenada no Supabase.

### Operações e filtros

| Método             | Rota                       | Descrição                              |
| ------------------- | -------------------------- | ---------------------------------------- |
| `GET`             | `/api/v1/products/`      | Lista produtos da loja em`X-Store-ID`. |
| `POST`            | `/api/v1/products/`      | Cria produto da loja atual.              |
| `GET`             | `/api/v1/products/{id}/` | Consulta produto da loja atual.          |
| `PUT` / `PATCH` | `/api/v1/products/{id}/` | Atualiza produto; pode trocar a imagem.  |
| `DELETE`          | `/api/v1/products/{id}/` | Exclui produto e sua imagem.             |

Filtros: `?category=1`, `?price=9.90` e `?name=cola`. Paginação: `?page=2&page_size=40`.

---

## 🧾 Orders — pedidos

Todas as rotas de pedidos exigem autenticação e `X-Store-ID`.

- Um usuário que possui perfil de cliente vê **somente seus pedidos** na loja selecionada.
- Um usuário sem esse perfil vê os pedidos da loja selecionada.
- Na criação, `store` vem do header e `customer` vem do usuário autenticado: **não envie esses dois campos**.

### ⚠️ Campo obrigatório `itens`

O campo `itens` é um JSON obrigatório e precisa ser enviado como uma **lista de objetos**, mantendo esta estrutura para cada produto:

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

Em `multipart/form-data`, envie o mesmo conteúdo serializado como texto no campo `itens`:

```text
itens=[{"id":5,"name":"Mouse","price":19.00,"quantity":2}]
```

> ✅ Não envie um objeto solto nem apenas IDs. Sempre envie um array `[]`, mesmo que o pedido tenha somente um item.

### Criar pedido

`POST /api/v1/orders/` · 🔒 Autenticado

```json
{
  "name_customer": "João Silva",
  "phone": "11999999999",
  "address": "Rua das Flores",
  "house_number": "123",
  "observation": "Entregar na portaria",
  "latitude": "-23.550520",
  "longitude": "-46.633308",
  "subtotal": "38.00",
  "rate_delivery": "5.00",
  "total": "43.00",
  "remaining": "0.00",
  "payment_method": "pix",
  "itens": [
    {
      "id": 5,
      "name": "Mouse",
      "price": 19.00,
      "quantity": 2
    }
  ]
}
```

Campos importantes:

| Campo                                                          | Descrição                                                         |
| -------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name_customer`, `phone`, `address`                      | Dados de entrega obrigatórios.                                     |
| `house_number`, `observation`, `latitude`, `longitude` | Dados complementares opcionais.                                     |
| `subtotal`, `rate_delivery`, `total`                     | Valores monetários com duas casas decimais.                        |
| `remaining`                                                  | Troco necessário. Use`0.00` quando não houver.                  |
| `payment_method`                                             | Forma de pagamento, por exemplo`pix`, `dinheiro` ou `cartao`. |
| `itens`                                                      | Lista JSON de itens, conforme estrutura acima.                      |
| `code`, `status`, `store`, `customer`                  | Preenchidos pelo servidor.                                          |

O pedido nasce com status `pendente` e recebe um código de entrega.

### Consultar e alterar pedidos

| Método             | Rota                     | Descrição                             |
| ------------------- | ------------------------ | --------------------------------------- |
| `GET`             | `/api/v1/orders/`      | Lista pedidos dentro da loja do header. |
| `POST`            | `/api/v1/orders/`      | Cria pedido.                            |
| `GET`             | `/api/v1/orders/{id}/` | Detalha pedido.                         |
| `PUT` / `PATCH` | `/api/v1/orders/{id}/` | Atualiza os campos permitidos.          |
| `DELETE`          | `/api/v1/orders/{id}/` | Exclui pedido.                          |

Filtros disponíveis: `?created_at=...`, `?code=AB12` e `?total=43.00`.

### Confirmar entrega

`POST /api/v1/orders/{id}/confirm-delivery` · 🔒 Autenticado

> Atenção: esta rota específica **não** possui barra final.

```json
{ "code": "a1b2" }
```

O código deve ter exatamente quatro caracteres e precisa coincidir com o código gerado para o pedido. Somente pedidos `pendente` podem ser confirmados. Em caso de sucesso, o status muda para `entregue`.

```json
{ "detail": "Entrega confirmada com sucesso." }
```

---

## 💰 Sales — vendas

Uma venda é vinculada a um pedido, à conta autenticada e à loja enviada em `X-Store-ID`. A API define `account` e `store` no backend para impedir que o frontend atribua vendas a outra loja.

### Criar venda

`POST /api/v1/sales/` · 🔒 Proprietário da loja

```json
{
  "order": 42,
  "subtotal": "38.00",
  "rate_delivery": "5.00",
  "total": "43.00",
  "remaining": "0.00",
  "payment_method": "pix",
  "collaborator": "Maria",
  "observation": "Venda gerada no caixa",
  "status": true
}
```

Cada pedido aceita somente uma venda. `order` é uma relação um-para-um.

### Operações disponíveis

| Método                                 | Rota                    |
| --------------------------------------- | ----------------------- |
| `GET`, `POST`                       | `/api/v1/sales/`      |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/api/v1/sales/{id}/` |

Em todas elas envie `X-Store-ID`. A loja precisa pertencer ao usuário autenticado, ou a API retornará `403 Forbidden`.

---

## 📌 Exemplo completo com cURL

### 1. Login

```bash
curl -X POST "http://localhost:8000/api/v1/authentication/token/" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@local.test","password":"12345678"}'
```

### 2. Listar produtos de uma loja

```bash
curl "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "X-Store-ID: ABC123"
```

### 3. Criar pedido com itens

```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "X-Store-ID: ABC123" \
  -H "Content-Type: application/json" \
  -d '{
    "name_customer":"João Silva",
    "phone":"11999999999",
    "address":"Rua das Flores",
    "house_number":"123",
    "subtotal":"38.00",
    "rate_delivery":"5.00",
    "total":"43.00",
    "remaining":"0.00",
    "payment_method":"pix",
    "itens":[{"id":5,"name":"Mouse","price":19.00,"quantity":2}]
  }'
```

---

## 🧪 Coleção Postman

O projeto inclui uma coleção pronta em [postman/My_Store_API.postman_collection.json](postman/My_Store_API.postman_collection.json).

Importe-a no Postman, execute **Login - obter JWT** e preencha as variáveis da coleção (`store_id`, `category_id`, `customer_id`, `order_id` e `product_id`) à medida que criar os recursos. A coleção já envia automaticamente o `access_token` retornado pelo login.

---

## ⚠️ Respostas de erro mais comuns

| Status               | Significado comum                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| `400 Bad Request`  | Campo ausente/inválido, imagem inválida, código de entrega incorreto ou pedido não pendente. |
| `401 Unauthorized` | Token ausente, expirado ou inválido.                                                            |
| `403 Forbidden`    | Falta do`X-Store-ID`, loja inexistente/sem acesso ou ação sem permissão.                    |
| `404 Not Found`    | Recurso não encontrado dentro do escopo atual.                                                  |

## 🧰 Tecnologias

- Django 6 e Django REST Framework;
- Simple JWT para autenticação;
- PostgreSQL configurado via `DATABASE_URL`;
- Supabase Storage para imagens de lojas, clientes e produtos;
- `django-filter` para filtros;
- WhiteNoise para arquivos estáticos e Jazzmin no painel administrativo.

---

<div align="center">
  Feito para simplificar a operação de lojas. 🛒
</div>
