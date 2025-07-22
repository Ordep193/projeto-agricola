document.addEventListener("DOMContentLoaded", function () {
  const estadoSelect = document.getElementById("estado");
  const cidadeSelect = document.getElementById("cidade");

  const estadoSelecionado = estadoSelect.getAttribute("data-uf");
  const cidadeSelecionada = cidadeSelect.getAttribute("data-cidade");

  // Carrega os estados
  fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome")
    .then((res) => res.json())
    .then((estados) => {
      estados.forEach((uf) => {
        const option = document.createElement("option");
        option.value = uf.sigla;
        option.textContent = uf.nome;
        estadoSelect.appendChild(option);
      });

      if (estadoSelecionado) {
        estadoSelect.value = estadoSelecionado;
        carregarCidades(estadoSelecionado, cidadeSelecionada);
      }
    });

  // Quando o estado muda, carregar cidades
  estadoSelect.addEventListener("change", function () {
    const uf = this.value;
    carregarCidades(uf);
  });

  function carregarCidades(uf, cidadeParaSelecionar = null) {
    cidadeSelect.innerHTML = "<option>Carregando...</option>";

    fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`)
      .then((res) => res.json())
      .then((cidades) => {
        cidadeSelect.innerHTML = "";
        cidades.forEach((c) => {
          const option = document.createElement("option");
          option.value = c.nome;
          option.textContent = c.nome;
          cidadeSelect.appendChild(option);
        });

        if (cidadeParaSelecionar) {
          cidadeSelect.value = cidadeParaSelecionar;
        }
      });
  }
});
