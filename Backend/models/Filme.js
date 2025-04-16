const mongoose = require("mongoose");

const FilmeSchema = new mongoose.Schema({
  title: String,
  year: Number,
  duration: Number,
  MPA: String,
  rating: Number,
  votes: Number,
  meta_score: Number,
  description: String,
  movie_link: String,
  writers: [String],
  directors: [String],
  stars: [String],
  languages: [String],
  oscar_nominated: Boolean,
  oscar_winner: Boolean,
  oscar_category: String,
  globe_nominated: Boolean,
  globe_winner: Boolean,
  globe_category: String,
});

module.exports = mongoose.model("Filme", FilmeSchema);
