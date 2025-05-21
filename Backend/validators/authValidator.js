const { check } = require('express-validator');

const validarRegistro = [
  check('nome', 'O nome é obrigatório').not().isEmpty(),
  check('email', 'O email é obrigatório').isEmail(),
  check('senha', 'A senha deve ter no mínimo 6 caracteres').isLength({
    min: 6,
  }),
  check('confirmarSenha', 'As senhas não conferem').custom((value, { req }) => {
    if (value !== req.body.senha) {
      throw new Error('As senhas não conferem');
    }
    return true;
  }),
];

const validarLogin = [
  check('email', 'O email é obrigatório').isEmail(),
  check('senha', 'A senha é obrigatória').not().isEmpty(),
];

module.exports = {
  validarRegistro,
  validarLogin,
};
