const jwt = require('jsonwebtoken');
const Usuario = require('../models/Usuario');

const proteger = async (req, res, next) => {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith('Bearer ')) {
    return res.status(401).json({ erro: 'Token não fornecido' });
  }

  const token = auth.split(' ')[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.usuario = await Usuario.findById(decoded.id).select('-senha');
    next();
  } catch (err) {
    res.status(401).json({ erro: 'Token inválido' });
  }
};

module.exports = proteger;
