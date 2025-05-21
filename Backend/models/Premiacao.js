const mongoose = require('mongoose');

const PremiacaoSchema = new mongoose.Schema({
  nome: { 
    type: String, 
    required: true,
    enum: ['Oscar', 'Globo de Ouro', 'BAFTA', 'Outros'] 
  },
  ano: { 
    type: Number, 
    required: true,
    min: 1929,
    max: new Date().getFullYear() 
  },
  categoria: { 
    type: String, 
    required: true 
  },
  vencedor: { 
    type: Boolean, 
    required: true,
    default: false 
  },
  filme: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'Filme',
    required: true 
  },
  createdAt: { 
    type: Date, 
    default: Date.now 
  }
});

PremiacaoSchema.index({ nome: 1, ano: 1, categoria: 1 }, { unique: true });