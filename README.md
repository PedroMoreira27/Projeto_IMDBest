## 🎬 API RESTful - Filmes & Premiações

Esta é a API backend do projeto de previsão de prêmios para filmes, construída com **Node.js**, **Express** e **MongoDB**. Ela serve dados sobre filmes, usuários e premiações (Oscar e Globo de Ouro), permitindo também o envio de novos filmes pelo app para posterior análise por aprendizado de máquina.

---

### ✅ Funcionalidades

- Cadastro e login de usuários (com JWT)
- Listagem de filmes e premiações
- Envio de novos filmes para análise
- API protegida por autenticação

---

### 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/VBaldochi/Projeto_IMDBest
cd Projeto_IMDBest

# Instale as dependências
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

---

#### 🏆 Premiações

##### `GET /api/premiacoes`

Lista todas as premiações cadastradas.

##### `POST /api/premiacoes` 🔐

```json
{
  "ano": 2024,
  "tipo": "Oscar",
  "filmeVencedor": "Oppenheimer"
}
```

---

### 🛠 Tecnologias

- Node.js + Express
- MongoDB + Mongoose
- JWT (Auth)
- Dotenv
- CORS

---

### 📱 Frontend

O app será desenvolvido em **.NET MAUI** e consumirá esta API.

