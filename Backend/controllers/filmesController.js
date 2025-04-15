const Filme = require('../models/Filme');

exports.listarFilmes = async (req, res) => {
  const { lancadosDepois } = req.query;
  const filtro = lancadosDepois ? { dataLancamento: { $gt: new Date(lancadosDepois) } } : {};

  try {
    const filmes = await Filme.find(filtro);
    res.json(filmes);
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao buscar filmes' });
  }
};

exports.criarFilme = async (req, res) => {
  try {
    const novoFilme = new Filme({ ...req.body, enviadoPorUsuario: true });
    await novoFilme.save();
    res.status(201).json(novoFilme);
  } catch (err) {
    res.status(400).json({ erro: 'Erro ao cadastrar filme' });
  }
};
