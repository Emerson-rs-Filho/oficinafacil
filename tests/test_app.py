import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.models import db  # noqa: E402
from app.models.ordem_servico import OrdemServico  # noqa: E402
from config import TestConfig  # noqa: E402


@pytest.fixture
def cliente_http():
    app = create_app(TestConfig)
    with app.test_client() as c:
        with app.app_context():
            yield c
            db.drop_all()


def logar(c):
    c.post("/cadastro", data={"nome": "Teste", "email": "t@t.com", "senha": "123456"})
    return c.post("/login", data={"email": "t@t.com", "senha": "123456"}, follow_redirects=True)


def test_exige_login(cliente_http):
    r = cliente_http.get("/clientes/")
    assert r.status_code == 302 and "/login" in r.location


def test_login_invalido(cliente_http):
    r = cliente_http.post("/login", data={"email": "x@x.com", "senha": "errada"})
    assert "inválidos" in r.get_data(as_text=True)


def test_fluxo_completo(cliente_http):
    assert "Agenda de hoje" in logar(cliente_http).get_data(as_text=True)

    r = cliente_http.post("/clientes/novo", data={"nome": "Ana", "telefone": "(48) 99999-0000"},
                          follow_redirects=True)
    assert "Ana" in r.get_data(as_text=True)

    r = cliente_http.post("/veiculos/novo", data={"cliente_id": "1", "placa": "abc-1d23",
                          "marca": "Fiat", "modelo": "Uno", "ano": "2010"}, follow_redirects=True)
    assert "ABC1D23" in r.get_data(as_text=True)

    r = cliente_http.post("/ordens/nova", data={"veiculo_id": "1", "descricao": "Troca de óleo",
                          "data_agendada": "2026-11-20T10:00", "status": "Agendada",
                          "valor": "1.250,50"}, follow_redirects=True)
    texto = r.get_data(as_text=True)
    assert "Troca de óleo" in texto and "R$ 1.250,50" in texto

    r = cliente_http.post("/ordens/1/status", json={"status": "Concluída"})
    assert r.get_json()["status"] == "Concluída"
    assert db.session.get(OrdemServico, 1).status == "Concluída"

    r = cliente_http.get("/")
    assert "R$ 1.250,50" in r.get_data(as_text=True)


def test_placa_invalida(cliente_http):
    logar(cliente_http)
    cliente_http.post("/clientes/novo", data={"nome": "Ana", "telefone": "1"})
    r = cliente_http.post("/veiculos/novo", data={"cliente_id": "1", "placa": "12",
                          "marca": "Fiat", "modelo": "Uno"})
    assert "Placa inválida" in r.get_data(as_text=True)


def test_status_invalido(cliente_http):
    logar(cliente_http)
    r = cliente_http.post("/ordens/99/status", json={"status": "X"})
    assert r.status_code == 404
