const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");
const controller = require("../controllers/filmes");
const { validarCriacaoFilme } = require("../middleware/validarFilme");
const { validarCriacaoPremiacao } = require("../middleware/validarPremiacao");

// Rotas de Filmes
router.get("/", controller.listarFilmes);
router.post("/", auth, validarCriacaoFilme, controller.criarFilme);

// Rotas de Integração
router.post("/verificar", auth, controller.verificarPremiacao);
router.post("/classificar", auth, controller.classificarFilme);

// Rotas de Premiações
router.get("/premiacoes", controller.listarPremiacoes);
router.post("/premiacoes", auth, validarCriacaoPremiacao, controller.criarPremiacao);

module.exports = router;