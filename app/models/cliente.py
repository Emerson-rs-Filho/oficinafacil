from datetime import datetime

from app.models import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    cpf = db.Column(db.String(14), unique=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    veiculos = db.relationship(
        "Veiculo", back_populates="cliente", cascade="all, delete-orphan"
    )
