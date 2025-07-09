// controllers/authController.js
import { produtores } from "./ProdutoresTestes.js";
import { coordenadores } from "./coordenadorController.js";

exports.login = (req, res) => {
  const { email, senha } = req.body;

  coordenadores.forEach(function(coordenador) {
    if (email === coordenador.email && senha === coordenador.senha) {
      req.session.user = { id: coordenador.id, email: coordenador.email }; // Armazena informações do usuário na sessão
      produtoresDoCoordenador = listarProdutores(coordenador.id)
      res.render('servicosCoordenador',{ produtores: produtoresDoCoordenador });
    }
  })
  res.redirect('/login?error=1');
};

exports.isAuthenticated = (req, res, next) => {
  if (req.session.user) {
    return next();
  }
  
  res.redirect('/login');
};

listarProdutores = (id) => {

  const produtoresDoCoordenador = produtores.filter(
    produtor => produtor.idCoordenador === id
  );
  return produtoresDoCoordenador
};

exports.detalhesProdutor = (req, res) => {
  const id = parseInt(req.params.id);

  console.log("teste: "+id);
  
  const produtor = produtores.find(p => p.id === id);

  if (!produtor) {
    return res.status(404).send('Produtor não encontrado');
  }

  res.render('detalhes-produtor', { produtor: produtor });
};
