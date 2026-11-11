"""Fábrica da aplicação OficinaFácil.

Organização MVC:
- app/models       -> Model (entidades e acesso ao banco via SQLAlchemy)
- app/controllers  -> Controller (rotas e regras de negócio, em Blueprints)
- app/views        -> View (templates HTML/Jinja2, CSS e JavaScript)
"""
from flask import Flask
from flask_login import LoginManager

from config import Config
from app.models import db
from app.models.usuario import Usuario

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar o sistema."
login_manager.login_message_category = "aviso"


@login_manager.user_loader
def carregar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.veiculo_controller import veiculo_bp
    from app.controllers.ordem_controller import ordem_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(veiculo_bp)
    app.register_blueprint(ordem_bp)

    @app.template_filter("moeda")
    def formatar_moeda(valor):
        valor = valor or 0
        texto = f"{valor:,.2f}"
        return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")

    @app.template_filter("data_br")
    def formatar_data(data):
        return data.strftime("%d/%m/%Y %H:%M") if data else "-"

    with app.app_context():
        db.create_all()

    return app
