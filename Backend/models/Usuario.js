const mongoose = require('mongoose');

const UsuarioSchema = new mongoose.Schema({
  nome: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  senha: {
    type: String,
    required: true,
  },
  dataCriacao: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Usuario', UsuarioSchema);

// controllers/authController.js
const jwt = require('jsonwebtoken');
const Usuario = require('../models/Usuario');

const gerarToken = (usuario) => {
  return jwt.sign(
    { id: usuario._id, email: usuario.email },
    process.env.JWT_SECRET,
    {
      expiresIn: '7d',
    },
  );
};

exports.registrar = async (req, res) => {
  try {
    const usuario = new Usuario(req.body);
    await usuario.save();
    const token = gerarToken(usuario);
    res.status(201).json({
      usuario: { id: usuario._id, nome: usuario.nome, email: usuario.email },
      token,
    });
  } catch (err) {
    console.error(err);
    res.status(400).json({ erro: 'Erro ao registrar usuário.' });
  }
};

exports.login = async (req, res) => {
  const { email, senha } = req.body;
  try {
    const usuario = await Usuario.findOne({ email });
    if (!usuario || !(await usuario.validarSenha(senha))) {
      return res.status(401).json({ erro: 'Credenciais inválidas' });
    }
    const token = gerarToken(usuario);
    res.json({
      usuario: { id: usuario._id, nome: usuario.nome, email: usuario.email },
      token,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ erro: 'Erro ao fazer login' });
  }
};
