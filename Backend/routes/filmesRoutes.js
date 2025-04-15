const express = require('express');
const router = express.Router();
const proteger = require('../middlewares/authMiddleware');
const { listarFilmes, criarFilme } = require('../controllers/filmesController');

router.get('/', listarFilmes);
router.post('/', proteger, criarFilme); // Só usuários autenticados podem cadastrar

module.exports = router;
