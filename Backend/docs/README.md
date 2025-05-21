# Documentação do Backend

## Visão Geral

O backend é uma API RESTful construída com Node.js, Express e MongoDB. Ele gerencia filmes e premiações, permitindo operações CRUD e integração com uma API externa.

## Estrutura do Projeto

```
Backend/
├── controllers/     # Lógica de negócios e manipulação de requisições
├── models/          # Schemas do MongoDB
├── routes/          # Definição das rotas da API
├── middleware/      # Middlewares (autenticação, validação)
├── validators/      # Validação de dados
├── docs/            # Documentação (Swagger, README)
├── server.js        # Ponto de entrada da aplicação
└── .env             # Variáveis de ambiente
```

## Tecnologias Utilizadas

- **Node.js**: Runtime JavaScript
- **Express**: Framework web
- **MongoDB**: Banco de dados NoSQL
- **Mongoose**: ODM para MongoDB
- **Swagger**: Documentação da API
- **Axios**: Cliente HTTP para integração com API externa

## Configuração

1. **Instalação de Dependências**:

   ```bash
   npm install
   ```

2. **Variáveis de Ambiente**:
   Crie um arquivo `.env` na raiz do projeto com:

   ```
   MONGO_URI=mongodb://localhost:27017/IMDBest
   PORT=5000
   ```

3. **Iniciar o Servidor**:
   ```bash
   npm start
   ```

## Rotas da API

### Filmes

- **GET /api/filmes**: Lista todos os filmes (com filtros opcionais)
- **POST /api/filmes**: Cria um novo filme
- **POST /api/filmes/verificar**: Verifica premiação de um filme
- **POST /api/filmes/classificar**: Classifica um filme

### Premiações

- **GET /api/filmes/premiacoes**: Lista todas as premiações
- **POST /api/filmes/premiacoes**: Cria uma nova premiação

## Modelos

### Filme

- **title**: Título do filme (String, obrigatório)
- **year**: Ano de lançamento (Number, obrigatório)
- **duration**: Duração em minutos (Number)
- **MPA**: Classificação etária (String)
- **rating**: Avaliação (Number)
- **votes**: Número de votos (Number)
- **meta_score**: Pontuação meta (Number)
- **description**: Descrição (String)
- **movie_link**: Link do filme (String)
- **writers**: Roteiristas (Array de Strings)
- **directors**: Diretores (Array de Strings)
- **stars**: Atores (Array de Strings)
- **languages**: Idiomas (Array de Strings)
- **awards**: Premiações (Oscar e Globo de Ouro)
- **createdAt**: Data de criação (Date)
- **updatedAt**: Data de atualização (Date)

### Premiação

- **title**: Título da premiação (String)
- **year**: Ano da premiação (Number)
- **category**: Categoria (String)
- **winner**: Vencedor (Boolean)

## Middlewares

- **authMiddleware**: Autenticação de usuários
- **validarFilme**: Validação de dados de filmes
- **validarPremiacao**: Validação de dados de premiações

## Integração com API Externa

O backend se integra com uma API externa (FastAPI) para:

- Verificar premiações de filmes
- Classificar filmes

## Documentação Swagger

Acesse a documentação da API em:

```
http://localhost:5000/docs
```

## Tratamento de Erros

- Erros de validação retornam status 422
- Erros de banco de dados retornam status 500
- Erros de requisição retornam status 400

## Logs

- Logs de conexão com o MongoDB
- Logs de erros em operações críticas

## Próximos Passos

- Implementar testes automatizados
- Adicionar cache para melhorar performance
- Expandir funcionalidades de busca e filtros
