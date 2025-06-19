import { Produtor } from './produtor.js';

class Coordenador {
  #nome;
  #email;
  #senha;
  #id;
  #produtores = [];

  constructor(nome, email, senha, id) {
    this.#nome = nome;
    this.#email = email;
    this.#senha = senha;
    this.#id = id;
  }

  // Getters
  get nome() {
    return this.#nome;
  }

  get email() {
    return this.#email;
  }

  get senha() {
    return this.#senha;
  }

  get id() {
    return this.#id;
  }

  get produtores() {
    return [...this.#produtores];
  }

  // Setters
  set nome(value) {
    this.#nome = value;
  }

  set email(value) {
    this.#email = value;
  }

  set senha(value) {
    this.#senha = value;
  }

  set id(value) {
    this.#id = value;
  }

  // Métodos
  adicionarProdutor(produtor) {
    if (produtor instanceof Produtor) {
      this.#produtores.push(produtor);
    } else {
      console.warn('Objeto inválido ao adicionar produtor.');
    }
  }

  listarProdutores() {
    return this.#produtores.map(p => p.nome);
  }
}

export { Coordenador };
