const { body, validationResult } = require("express-validator");
exports.validarCriacaoFilme = [
  body('title').trim().notEmpty().withMessage('Título é obrigatório'),
  body('year')
    .isInt({ min: 1888, max: new Date().getFullYear() })
    .withMessage(`Ano deve estar entre 1888 e ${new Date().getFullYear()}`),
  body('duration').optional().isInt({ min: 1 }).withMessage('Duração deve ser em minutos e maior que 0'),
  body('MPA').optional().isIn(['G', 'PG', 'PG-13', 'R', 'NC-17', 'Passed', 'Approved']),
  body('rating').optional().isFloat({ min: 0, max: 10 }).withMessage('Rating deve estar entre 0 e 10'),
  body('movie_link').optional().isURL().withMessage('URL do filme inválida'),
  body('writers').optional().isArray().withMessage('Escritores devem ser um array'),
  body('directors').optional().isArray().withMessage('Diretores devem ser um array'),
  body('stars').optional().isArray().withMessage('Elenco deve ser um array'),
  body('languages').optional().isArray().withMessage('Idiomas devem ser um array'),
  
  // Validação para campos de premiação legados (se necessário)
  body('oscar_nominated').optional().isBoolean(),
  body('oscar_winner').optional().isBoolean(),
  body('oscar_category').optional().isString(),
  body('globe_nominated').optional().isBoolean(),
  body('globe_winner').optional().isBoolean(),
  body('globe_category').optional().isString(),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ erros: errors.array() });
    }
    next();
  }
];