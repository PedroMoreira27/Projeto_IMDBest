const mongoose = require('mongoose');

const premiacaoSchema = new mongoose.Schema({
  nome: String, // "Oscar" ou "Globo de Ouro"
  ano: Number,
  categoria: String,
  vencedor: Boolean,
  filme: String, // Nome do filme
}, { timestamps: true });

module.exports = mongoose.model('Premiacao', premiacaoSchema);
