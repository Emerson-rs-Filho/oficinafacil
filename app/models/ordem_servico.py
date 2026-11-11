from datetime import datetime

from app.models import db

STATUS = ["Agendada", "Em andamento", "Concluída", "Cancelada"]


class OrdemServico(db.Model):
    __tablename__ = "ordens_servico"

    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_agendada = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Agendada")
    valor = db.Column(db.Numeric(10, 2), default=0)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    veiculo = db.relationship("Veiculo", back_populates="ordens")

    @property
    def classe_status(self):
        return {
            "Agendada": "agendada",
            "Em andamento": "andamento",
            "Concluída": "concluida",
            "Cancelada": "cancelada",
        }.get(self.status, "")
