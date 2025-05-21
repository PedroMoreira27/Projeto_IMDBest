const mongoose = require('mongoose');

const FilmeSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, index: true },
    year: {
      type: Number,
      required: true,
      min: 1888,
      max: new Date().getFullYear(),
    },
    duration: { type: Number, min: 1 }, // em minutos
    MPA: {
      type: String,
      enum: ['G', 'PG', 'PG-13', 'R', 'NC-17', 'Passed', 'Approved'],
    },
    rating: { type: Number, min: 0, max: 10 },
    votes: { type: Number, min: 0 },
    meta_score: { type: Number, min: 0, max: 100 },
    description: String,
    movie_link: { type: String, match: /^https?:\/\/.+/ },
    writers: [{ type: String }], // Array de strings
    directors: [{ type: String }], // Array de strings
    stars: [{ type: String }], // Array de strings
    languages: [{ type: String }], // Array de strings
    awards: {
      oscar: {
        nominated: Boolean,
        winner: Boolean,
        category: String,
      },
      goldenGlobe: {
        nominated: Boolean,
        winner: Boolean,
        category: String,
      },
    },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
  },
  {
    collection: 'IMDBest', //
  },
);

// Atualiza o campo updatedAt antes de salvar
FilmeSchema.pre('save', function (next) {
  this.updatedAt = new Date();
  next();
});

module.exports = mongoose.model('Filme', FilmeSchema);
