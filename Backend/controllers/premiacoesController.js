const Premiacao = require('../models/Premiacao');

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
    res.status(400).json({ erro: 'Erro ao cadastrar premiação' });
  }
};