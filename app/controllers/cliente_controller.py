from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.models import db
from app.models.cliente import Cliente

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


def _obter(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if not cliente:
        abort(404)
    return cliente


def _validar(form, cliente_id=None):
    erros = []
    if not form.get("nome", "").strip():
        erros.append("O nome é obrigatório.")
    if not form.get("telefone", "").strip():
        erros.append("O telefone é obrigatório.")
    cpf = form.get("cpf", "").strip()
    if cpf:
        existente = Cliente.query.filter_by(cpf=cpf).first()
        if existente and existente.id != cliente_id:
            erros.append("Já existe um cliente com este CPF.")
    return erros


def _preencher(cliente, form):
    cliente.nome = form["nome"].strip()
    cliente.telefone = form["telefone"].strip()
    cliente.email = form.get("email", "").strip() or None
    cliente.cpf = form.get("cpf", "").strip() or None


@cliente_bp.route("/")
@login_required
def listar():
    busca = request.args.get("q", "").strip()
    consulta = Cliente.query
    if busca:
        termo = f"%{busca}%"
        consulta = consulta.filter(
            Cliente.nome.ilike(termo) | Cliente.telefone.ilike(termo) | Cliente.cpf.ilike(termo)
        )
    clientes = consulta.order_by(Cliente.nome).all()
    return render_template("clientes/lista.html", clientes=clientes, busca=busca)


@cliente_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        erros = _validar(request.form)
        if not erros:
            cliente = Cliente()
            _preencher(cliente, request.form)
            db.session.add(cliente)
            db.session.commit()
            flash("Cliente cadastrado com sucesso.", "sucesso")
            return redirect(url_for("clientes.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template("clientes/form.html", cliente=None, form=request.form)


@cliente_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(cliente_id):
    cliente = _obter(cliente_id)
    if request.method == "POST":
        erros = _validar(request.form, cliente.id)
        if not erros:
            _preencher(cliente, request.form)
            db.session.commit()
            flash("Cliente atualizado.", "sucesso")
            return redirect(url_for("clientes.listar"))
        for erro in erros:
            flash(erro, "erro")
    return render_template("clientes/form.html", cliente=cliente, form=request.form)


@cliente_bp.route("/<int:cliente_id>/excluir", methods=["POST"])
@login_required
def excluir(cliente_id):
    cliente = _obter(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente excluído.", "sucesso")
    return redirect(url_for("clientes.listar"))
