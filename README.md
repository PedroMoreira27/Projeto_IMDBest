## 🎬 API RESTful - Filmes & Premiações

Esta é a API backend do projeto de previsão de prêmios para filmes, construída com **Node.js**, **Express** e **MongoDB**. Ela serve dados sobre filmes, usuários e premiações (Oscar e Globo de Ouro), permitindo também o envio de novos filmes pelo app para posterior análise por aprendizado de máquina.

---

### ✅ Funcionalidades

- Cadastro e login de usuários (com JWT)
- Listagem de filmes e premiações
- Envio de novos filmes para análise
- API protegida por autenticação

---

### 🚀 Instalação da API (Backend)

```bash
# Clone o repositório
cd backend
npm install

# Crie um arquivo .env com as seguintes variáveis:
```

`.env`

```
PORT=5000
MONGO_URI=mongodb://localhost:27017/filmes-db
JWT_SECRET=sua-chave-secreta
```

```bash
# Inicie o servidor
npm start
```

---

### 📡 Rotas da API

---

#### 🔐 Autenticação

##### `POST /api/auth/registrar`

```json
{
  "nome": "João",
  "email": "joao@email.com",
  "senha": "123456"
}
```

##### `POST /api/auth/login`

```json
{
  "email": "joao@email.com",
  "senha": "123456"
}
```

**Resposta (ambos):**

```json
{
  "usuario": {
    "_id": "abc123",
    "nome": "João",
    "email": "joao@email.com"
  },
  "token": "jwt-token-aqui"
}
```

---

#### 🎞️ Filmes

##### `GET /api/filmes`

Lista todos os filmes. Pode receber o parâmetro `lancadosDepois`:

`GET /api/filmes?lancadosDepois=2024-03-10`

##### `POST /api/filmes` 🔐

Envio de novo filme para análise (necessita token JWT):

```http
Authorization: Bearer seu-jwt-token
```

```json
{
  "titulo": "Filme Incrível",
  "ano": 2025,
  "diretor": "Fulano de Tal",
  "dataLancamento": "2025-04-01",
  "genero": "Drama",
  "notaIMDB": 8.4
}
```

> ⚠️ Filmes enviados ainda não concorreram a premiações. O sistema futuramente analisará esses dados para prever possíveis indicações e vitórias.

---

#### 🏆 Premiações

##### `GET /api/premiacoes`

Lista todas as premiações cadastradas (Oscar, Globo de Ouro). Pode ser usada para determinar o último prêmio ocorrido.

> 🔒 A criação de premiações é uma funcionalidade administrativa e não está disponível publicamente via API.

---

### 🛠 Tecnologias Backend

- Node.js + Express
- MongoDB + Mongoose
- JWT (Auth)
- Dotenv
- CORS

---

### 📱 App Mobile - .NET MAUI

O aplicativo mobile será desenvolvido em **.NET MAUI**, com foco em:

- Interface para login e cadastro de usuário
- Tela de listagem dos filmes e seus dados (IMDB, duração, etc.)
- Tela para envio de novos filmes para análise
- Visualização das premiações e últimos vencedores

#### Instalação do App

```bash
cd frontend
# Abra no Visual Studio 2022 ou superior com suporte a MAUI
```

- Configure a plataforma desejada (Android, iOS, Windows)
- Rode o projeto: `Run > Start Debugging`

---

### 📦 Estrutura do Projeto

```
raiz-do-projeto/
├── backend/          # API Node.js (Express + MongoDB)
├── frontend/         # App .NET MAUI
├── README.md         # Este arquivo
```

---

### 📬 Contato

Dúvidas ou sugestões? Entre em contato com a equipe de desenvolvimento.

---

> Projeto acadêmico com fins de aprendizado. Utiliza dados públicos do IMDB, Oscar e Globo de Ouro.

