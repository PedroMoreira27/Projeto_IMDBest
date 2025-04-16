const express = require("express");
const router = express.Router();
const Filme = require("../models/Filme");
const auth = require("../middleware/auth");

router.get("/", async (req, res) => {
  const filmes = await Filme.find();
  res.json(filmes);
});

router.post("/", auth, async (req, res) => {
  try {
    const novoFilme = new Filme(req.body);
    await novoFilme.save();
    res.status(201).json(novoFilme);
  } catch (err) {
    res.status(400).json({ erro: err.message });
  }
});

module.exports = router;
