const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const Usuario = require('../models/Usuario');

const gerarToken = (usuario) => {
  return jwt.sign({ id: usuario._id }, process.env.JWT_SECRET, {
    expiresIn: '7d',
  });
};

exports.registrar = async (req, res) => {
  try {
    const { nome, email, senha } = req.body;

    // Verifica se o usuário já existe
    let usuario = await Usuario.findOne({ email });
    if (usuario) {
      return res.status(400).json({ msg: 'Usuário já existe' });
    }

    // Cria novo usuário
    usuario = new Usuario({
      nome,
      email,
      senha,
    });

    // Criptografa a senha
    const salt = await bcrypt.genSalt(10);
    usuario.senha = await bcrypt.hash(senha, salt);

    // Salva o usuário
    await usuario.save();

    // Cria e retorna o token
    const payload = {
      usuario: {
        id: usuario.id,
      },
    };

    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      { expiresIn: '24h' },
      (err, token) => {
        if (err) throw err;
        res.json({ token });
      },
    );
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Erro no servidor');
  }
};

exports.login = async (req, res) => {
  try {
    const { email, senha } = req.body;

    // Log da collection e do banco
    console.log('Collection usada:', Usuario.collection.name);
    console.log('Banco de dados:', Usuario.db.name);

    // Verifica se o usuário existe
    let usuario = await Usuario.findOne({ email });
    if (!usuario) {
      return res.status(400).json({ msg: 'Credenciais inválidas' });
    }

    // Verifica a senha
    const senhaCorreta = await bcrypt.compare(senha, usuario.senha);
    if (!senhaCorreta) {
      return res.status(400).json({ msg: 'Credenciais inválidas' });
    }

    // Cria e retorna o token
    const payload = {
      usuario: {
        id: usuario.id,
      },
    };

    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      { expiresIn: '24h' },
      (err, token) => {
        if (err) throw err;
        res.json({ token });
      },
    );
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Erro no servidor');
  }
};
