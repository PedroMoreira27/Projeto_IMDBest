require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const authRoutes = require('./routes/authRoutes');
const filmesRoutes = require('./routes/filmesRoutes');
const premiacoesRoutes = require('./routes/premiacoesRoutes');

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/filmes', filmesRoutes);
app.use('/api/premiacoes', premiacoesRoutes);

mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    app.listen(process.env.PORT || 5000, () =>
      console.log(`Servidor rodando na porta ${process.env.PORT || 5000}`)
    );
  })
  .catch(err => console.error('Erro ao conectar ao MongoDB:', err));
