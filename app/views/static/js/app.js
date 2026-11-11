// OficinaFácil — comportamento da interface (camada View)

document.addEventListener("DOMContentLoaded", () => {
  // Menu responsivo (celular)
  const botaoMenu = document.getElementById("menuToggle");
  const menu = document.getElementById("menu");
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", () => menu.classList.toggle("aberto"));
  }

  // Confirmação antes de excluir
  document.querySelectorAll("form[data-confirmar]").forEach((form) => {
    form.addEventListener("submit", (evento) => {
      if (!confirm(form.dataset.confirmar)) evento.preventDefault();
    });
  });

  // Máscaras de campos
  const mascaras = {
    telefone(v) {
      v = v.replace(/\D/g, "").slice(0, 11);
      if (v.length > 10) return v.replace(/(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
      if (v.length > 6) return v.replace(/(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
      if (v.length > 2) return v.replace(/(\d{2})(\d+)/, "($1) $2");
      return v;
    },
    cpf(v) {
      v = v.replace(/\D/g, "").slice(0, 11);
      return v
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    },
    placa(v) {
      return v.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 7);
    },
  };
  document.querySelectorAll("[data-mascara]").forEach((campo) => {
    const aplicar = mascaras[campo.dataset.mascara];
    campo.addEventListener("input", () => (campo.value = aplicar(campo.value)));
  });

  // Troca rápida de status da ordem de serviço (sem recarregar a página)
  document.querySelectorAll(".seletor-status").forEach((seletor) => {
    let anterior = seletor.value;
    seletor.addEventListener("change", async () => {
      try {
        const resposta = await fetch(seletor.dataset.url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: seletor.value }),
        });
        if (!resposta.ok) throw new Error();
        const dados = await resposta.json();
        seletor.className = `seletor-status selo selo-${dados.classe}`;
        anterior = dados.status;
      } catch {
        alert("Não foi possível alterar o status. Tente novamente.");
        seletor.value = anterior;
      }
    });
  });
});
