class Produtor {
    constructor(id,nome, terreno, cidade, idade, talhoes = [],idCoordenador) {
        this.id = id;
        this.nome = nome;
        this.terreno = terreno;
        this.cidade = cidade;
        this.idade = idade;
        this.talhao = talhoes;
        this.idCoordenador = idCoordenador;
    }

    setId = (id) => {
        this.id = id;
    }
    getId = () => {
        return this.id;
    }

    setNome = (nome) => {
        this.nome = nome;
    }
    getNome = () => {
        return this.nome;
    }

    setTerreno = (terreno) => {
        this.terreno = terreno;
    }
    getTerreno = () => {
        return this.terreno;
    }

    setCidade = (cidade) => {
        this.cidade = cidade;
    }
    getCidade = () => {
        return this.cidade;
    }

    setIdade = (idade) => {
        this.idade = idade;
    }
    getIdade = () => {
        return this.idade;
    }

    setTalhao = (talhao) => {
        this.talhao.push(talhao);
    }
    getTalhao = () => {
        return this.talhao;
    }

    setIdCoordenador = (id) => {
        this.idCoordenador = id;
    }
    getIdCoordenador = () => {
        return this.idCoordenador;
    }
}

export { Produtor };