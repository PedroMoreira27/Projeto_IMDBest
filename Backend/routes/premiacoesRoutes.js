const express = require('express');
const router = express.Router();
const proteger = require('../middlewares/authMiddleware');
const { listarPremiacoes, criarPremiacao } = require('../controllers/premiacoesController');

router.get('/', listarPremiacoes);
router.post('/', proteger, criarPremiacao); // Exige login

module.exports = router;
