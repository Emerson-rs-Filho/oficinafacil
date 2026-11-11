from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importa os modelos para que o SQLAlchemy registre as tabelas
from app.models.usuario import Usuario  # noqa: E402,F401
from app.models.cliente import Cliente  # noqa: E402,F401
from app.models.veiculo import Veiculo  # noqa: E402,F401
from app.models.ordem_servico import OrdemServico  # noqa: E402,F401
