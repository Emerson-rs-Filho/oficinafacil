from datetime import datetime, time

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.models import db
from app.models.cliente import Cliente
from app.models.ordem_servico import OrdemServico
from app.models.veiculo import Veiculo

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    hoje = datetime.now().date()
    inicio, fim = datetime.combine(hoje, time.min), datetime.combine(hoje, time.max)

    agenda_hoje = (
        OrdemServico.query.filter(OrdemServico.data_agendada.between(inicio, fim))
        .order_by(OrdemServico.data_agendada)
        .all()
    )
    faturamento = (
        db.session.query(func.coalesce(func.sum(OrdemServico.valor), 0))
        .filter(OrdemServico.status == "Concluída")
        .scalar()
    )
    resumo = {
        "clientes": Cliente.query.count(),
        "veiculos": Veiculo.query.count(),
        "abertas": OrdemServico.query.filter(
            OrdemServico.status.in_(["Agendada", "Em andamento"])
        ).count(),
        "faturamento": float(faturamento or 0),
    }
    return render_template("dashboard.html", agenda_hoje=agenda_hoje, resumo=resumo)
