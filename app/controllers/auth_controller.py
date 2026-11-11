from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            return redirect(url_for("dashboard.index"))
        flash("E-mail ou senha inválidos.", "erro")

    return render_template("auth/login.html")


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or len(senha) < 6:
            flash("Preencha todos os campos. A senha deve ter ao menos 6 caracteres.", "erro")
        elif Usuario.query.filter_by(email=email).first():
            flash("Já existe um usuário com este e-mail.", "erro")
        else:
            usuario = Usuario(nome=nome, email=email)
            usuario.definir_senha(senha)
            db.session.add(usuario)
            db.session.commit()
            flash("Cadastro realizado! Faça login.", "sucesso")
            return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
