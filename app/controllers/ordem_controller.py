from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.models import db
from app.models.ordem_servico import STATUS, OrdemServico
from app.models.veiculo import Veiculo

ordem_bp = Blueprint("ordens", __name__, url_prefix="/ordens")


def _obter(ordem_id):
    ordem = db.session.get(OrdemServico, ordem_id)
    if not ordem:
        abort(404)
    return ordem


def _converter_valor(texto):
    texto = (texto or "0").strip().replace("R$", "").replace(" ", "")
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return Decimal(texto or "0")


def _validar(form):
    erros = []
    if not form.get("veiculo_id"):
        erros.append("Selecione o veículo.")
    if not form.get("descricao", "").strip():
        erros.append("Descreva o serviço.")
    try:
        datetime.strptime(form.get("data_agendada", ""), "%Y-%m-%dT%H:%M")
    except ValueError:
        erros.append("Informe data e hora válidas.")
    if form.get("status") not in STATUS:
        erros.append("Status inválido.")
    try:
        if _converter_valor(form.get("valor")) < 0:
            erros.append("O valor não pode ser negativo.")
    except InvalidOperation:
        erros.append("Valor inválido.")
    return erros


def _preencher(ordem, form):
    ordem.veiculo_id = int(form["veiculo_id"])
    ordem.descricao = form["descricao"].strip()
    ordem.data_agendada = datetime.strptime(form["data_agendada"], "%Y-%m-%dT%H:%M")
    ordem.status = form["status"]
    ordem.valor = _converter_valor(form.get("valor"))


@ordem_bp.route("/")
@login_required
def listar():
    status = request.args.get("status", "")
    consulta = OrdemServico.query
    if status in STATUS:
        consulta = consulta.filter_by(status=status)
    ordens = consulta.order_by(OrdemServico.data_agendada.desc()).all()
    return render_template(
        "ordens/lista.html", ordens=ordens, status_lista=STATUS, filtro=status
    )


@ordem_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    veiculos = Veiculo.query.order_by(Veiculo.placa).all()
    if request.method == "POST":
        erros = _validar(request.form)
        if not erros:
            ordem = OrdemServico()
            _preencher(ordem, request.form)
            db.session.add(ordem)
            db.session.commit()
            flash(f"Ordem de serviço nº {ordem.id} registrada.", "sucesso")
            return redirect(url_for("ordens.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template(
        "ordens/form.html", ordem=None, veiculos=veiculos,
        status_lista=STATUS, form=request.form,
    )


@ordem_bp.route("/<int:ordem_id>/editar", methods=["GET", "POST"])
@login_required
def editar(ordem_id):
    ordem = _obter(ordem_id)
    veiculos = Veiculo.query.order_by(Veiculo.placa).all()
    if request.method == "POST":
        erros = _validar(request.form)
        if not erros:
            _preencher(ordem, request.form)
            db.session.commit()
            flash("Ordem de serviço atualizada.", "sucesso")
            return redirect(url_for("ordens.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template(
        "ordens/form.html", ordem=ordem, veiculos=veiculos,
        status_lista=STATUS, form=request.form,
    )


@ordem_bp.route("/<int:ordem_id>/status", methods=["POST"])
@login_required
def alterar_status(ordem_id):
    """Rota usada pelo JavaScript (fetch) para mudar o status sem recarregar a página."""
    ordem = _obter(ordem_id)
    novo_status = (request.get_json(silent=True) or {}).get("status")
    if novo_status not in STATUS:
        return {"erro": "Status inválido"}, 400
    ordem.status = novo_status
    db.session.commit()
    return {"id": ordem.id, "status": ordem.status, "classe": ordem.classe_status}


@ordem_bp.route("/<int:ordem_id>/excluir", methods=["POST"])
@login_required
def excluir(ordem_id):
    ordem = _obter(ordem_id)
    db.session.delete(ordem)
    db.session.commit()
    flash("Ordem de serviço excluída.", "sucesso")
    return redirect(url_for("ordens.listar"))
