const mongoose = require('mongoose');

const filmeSchema = new mongoose.Schema({
  titulo: String,
  ano: Number,
  genero: [String],
  diretor: String,
  notaImdb: Number,
  dataLancamento: Date,
  indicacoes: {
    oscar: Boolean,
    globoDeOuro: Boolean
  },
  enviadoPorUsuario: Boolean
}, { timestamps: true });

module.exports = mongoose.model('Filme', filmeSchema);
