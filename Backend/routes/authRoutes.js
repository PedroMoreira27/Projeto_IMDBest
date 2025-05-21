const express = require('express');
const router = express.Router();
const { registrar, login } = require('../controllers/authController');
const { validarRegistro, validarLogin } = require('../validators/authValidator');
const validarCampos = require('../middlewares/validarCampos');

router.post('/registrar', validarRegistro, validarCampos, registrar);
router.post('/login', validarLogin, validarCampos, login);

module.exports = router;