const Filme = require('../models/Filme');
const Premiacao = require('../models/Premiacao');
const axios = require('axios');
const { validationResult } = require('express-validator');

const FASTAPI_BASE_URL = 'http://localhost:8000';

exports.listarFilmes = async (req, res) => {
  try {
    const { lancadosDepois, premiados } = req.query;
    const filtro = {};

    if (lancadosDepois) {
      filtro.year = { $gt: parseInt(lancadosDepois) };
    }

    if (premiados === 'true') {
      filtro.$or = [
        { 'awards.oscar.winner': true },
        { 'awards.goldenGlobe.winner': true },
      ];
    }

    const filmes = await Filme.find(filtro).sort({ year: -1 });
    res.json(filmes);
  } catch (err) {
    console.error('Erro ao buscar filmes:', err);
    res.status(500).json({ erro: 'Erro ao buscar filmes' });
  }
};

exports.criarFilme = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(422).json({ erros: errors.array() });
  }

  try {
    const filmeData = {
      ...req.body,
      awards: {
        oscar: {
          nominated: req.body.oscar_nominated || false,
          winner: req.body.oscar_winner || false,
          category: req.body.oscar_category || null,
        },
        goldenGlobe: {
          nominated: req.body.globe_nominated || false,
          winner: req.body.globe_winner || false,
          category: req.body.globe_category || null,
        },
      },
      enviadoPorUsuario: true,
    };

    const novoFilme = new Filme(filmeData);
    await novoFilme.save();
    res.status(201).json(novoFilme);
  } catch (err) {
    console.error('Erro ao criar filme:', err);
    res.status(400).json({ erro: err.message });
  }
};

exports.verificarPremiacao = async (req, res) => {
  const { title, year } = req.body;
  try {
    const response = await axios.post(
      `${FASTAPI_BASE_URL}/verificar-premiacao`,
      {
        title,
        year,
      },
    );
    res.json(response.data);
  } catch (err) {
    console.error('Erro FastAPI:', err.message);
    res
      .status(500)
      .json({ erro: 'Erro ao verificar premiação na API externa' });
  }
};

exports.classificarFilme = async (req, res) => {
  const { title, year, categorias } = req.body;
  try {
    const response = await axios.post(`${FASTAPI_BASE_URL}/classificar-filme`, {
      title,
      year,
      categorias,
    });
    res.json(response.data);
  } catch (err) {
    console.error('Erro FastAPI:', err.message);
    res.status(500).json({ erro: 'Erro ao classificar filme na API externa' });
  }
};

exports.listarPremiacoes = async (req, res) => {
  try {
    const premiacoes = await Premiacao.find();
    res.json(premiacoes);
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao buscar premiações' });
  }
};

exports.criarPremiacao = async (req, res) => {
  try {
    const nova = new Premiacao(req.body);
    await nova.save();
    res.status(201).json(nova);
  } catch (err) {
    res.status(400).json({ erro: err.message });
  }
};
