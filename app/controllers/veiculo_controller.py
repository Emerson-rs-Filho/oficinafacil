import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.models import db
from app.models.cliente import Cliente
from app.models.veiculo import Veiculo

veiculo_bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")

# Aceita placa antiga (ABC1234) e Mercosul (ABC1D23)
PADRAO_PLACA = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")


def _obter(veiculo_id):
    veiculo = db.session.get(Veiculo, veiculo_id)
    if not veiculo:
        abort(404)
    return veiculo


def _validar(form, veiculo_id=None):
    erros = []
    placa = form.get("placa", "").upper().replace("-", "").strip()
    if not PADRAO_PLACA.match(placa):
        erros.append("Placa inválida. Use o formato ABC1234 ou ABC1D23.")
    else:
        existente = Veiculo.query.filter_by(placa=placa).first()
        if existente and existente.id != veiculo_id:
            erros.append("Já existe um veículo com esta placa.")
    if not form.get("marca", "").strip() or not form.get("modelo", "").strip():
        erros.append("Marca e modelo são obrigatórios.")
    if not form.get("cliente_id"):
        erros.append("Selecione o cliente proprietário.")
    ano = form.get("ano", "").strip()
    if ano and (not ano.isdigit() or not 1950 <= int(ano) <= 2100):
        erros.append("Ano inválido.")
    return erros


def _preencher(veiculo, form):
    veiculo.placa = form["placa"].upper().replace("-", "").strip()
    veiculo.marca = form["marca"].strip()
    veiculo.modelo = form["modelo"].strip()
    veiculo.ano = int(form["ano"]) if form.get("ano", "").strip() else None
    veiculo.cliente_id = int(form["cliente_id"])


@veiculo_bp.route("/")
@login_required
def listar():
    busca = request.args.get("q", "").strip()
    consulta = Veiculo.query.join(Cliente)
    if busca:
        termo = f"%{busca}%"
        consulta = consulta.filter(
            Veiculo.placa.ilike(termo) | Veiculo.modelo.ilike(termo) | Cliente.nome.ilike(termo)
        )
    veiculos = consulta.order_by(Veiculo.placa).all()
    return render_template("veiculos/lista.html", veiculos=veiculos, busca=busca)


@veiculo_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    if request.method == "POST":
        erros = _validar(request.form)
        if not erros:
            veiculo = Veiculo()
            _preencher(veiculo, request.form)
            db.session.add(veiculo)
            db.session.commit()
            flash("Veículo cadastrado com sucesso.", "sucesso")
            return redirect(url_for("veiculos.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template(
        "veiculos/form.html", veiculo=None, clientes=clientes, form=request.form
    )


@veiculo_bp.route("/<int:veiculo_id>/editar", methods=["GET", "POST"])
@login_required
def editar(veiculo_id):
    veiculo = _obter(veiculo_id)
    clientes = Cliente.query.order_by(Cliente.nome).all()
    if request.method == "POST":
        erros = _validar(request.form, veiculo.id)
        if not erros:
            _preencher(veiculo, request.form)
            db.session.commit()
            flash("Veículo atualizado.", "sucesso")
            return redirect(url_for("veiculos.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template(
        "veiculos/form.html", veiculo=veiculo, clientes=clientes, form=request.form
    )


@veiculo_bp.route("/<int:veiculo_id>/excluir", methods=["POST"])
@login_required
def excluir(veiculo_id):
    veiculo = _obter(veiculo_id)
    db.session.delete(veiculo)
    db.session.commit()
    flash("Veículo excluído.", "sucesso")
    return redirect(url_for("veiculos.listar"))
