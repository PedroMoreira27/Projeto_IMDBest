const { body, validationResult } = require("express-validator");

exports.validarCriacaoPremiacao = [
  body("nome").isIn(["Oscar", "Globo de Ouro"]).withMessage("Premiação deve ser Oscar ou Globo de Ouro"),
  body("ano").isInt({ min: 1900 }).withMessage("Ano inválido"),
  body("categoria").notEmpty().withMessage("Categoria é obrigatória"),
  body("vencedor").isBoolean().withMessage("Vencedor deve ser true ou false"),
  body("filme").notEmpty().withMessage("Filme é obrigatório"),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ erros: errors.array() });
    }
    next();
  }
];
