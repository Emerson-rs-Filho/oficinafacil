from app.models import db


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(8), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="veiculos")
    ordens = db.relationship(
        "OrdemServico", back_populates="veiculo", cascade="all, delete-orphan"
    )

    @property
    def descricao(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
