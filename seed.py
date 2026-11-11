"""Cria o usuário de demonstração e dados de exemplo.

Uso:
  python seed.py           -> só insere se o banco estiver vazio (seguro rodar sempre)
  python seed.py --reset   -> APAGA tudo e recria os dados de exemplo

Login de demonstração:  admin@oficina.com / admin123
"""
import sys
from datetime import datetime, timedelta
from decimal import Decimal

from app import create_app
from app.models import db
from app.models.cliente import Cliente
from app.models.ordem_servico import OrdemServico
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo

app = create_app()

with app.app_context():
    if "--reset" in sys.argv:
        db.drop_all()
        db.create_all()

    if not Usuario.query.filter_by(email="admin@oficina.com").first():
        admin = Usuario(nome="Administrador", email="admin@oficina.com")
        admin.definir_senha("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Usuário de demonstração criado.")

    if Cliente.query.count() == 0:
        joao = Cliente(nome="João da Silva", telefone="(48) 99812-3344", cpf="123.456.789-00", email="joao@email.com")
        maria = Cliente(nome="Maria Oliveira", telefone="(48) 99677-1020")
        carlos = Cliente(nome="Carlos Pereira", telefone="(48) 3241-5566", email="carlos@email.com")
        db.session.add_all([joao, maria, carlos])

        gol = Veiculo(placa="QJX4B21", marca="Volkswagen", modelo="Gol", ano=2019, cliente=joao)
        onix = Veiculo(placa="RLA2C09", marca="Chevrolet", modelo="Onix", ano=2022, cliente=maria)
        hilux = Veiculo(placa="MKZ8812", marca="Toyota", modelo="Hilux", ano=2015, cliente=carlos)
        db.session.add_all([gol, onix, hilux])

        hoje = datetime.now().replace(minute=0, second=0, microsecond=0)
        db.session.add_all([
            OrdemServico(veiculo=gol, descricao="Troca de óleo e filtro", status="Agendada",
                         data_agendada=hoje.replace(hour=9), valor=Decimal("180.00")),
            OrdemServico(veiculo=onix, descricao="Revisão de freios", status="Em andamento",
                         data_agendada=hoje.replace(hour=14), valor=Decimal("450.00")),
            OrdemServico(veiculo=hilux, descricao="Alinhamento e balanceamento", status="Concluída",
                         data_agendada=hoje - timedelta(days=2), valor=Decimal("220.00")),
            OrdemServico(veiculo=gol, descricao="Diagnóstico de injeção eletrônica", status="Agendada",
                         data_agendada=hoje + timedelta(days=1), valor=Decimal("150.00")),
        ])
        db.session.commit()
        print("Dados de exemplo criados.")

    print("Pronto. Login: admin@oficina.com / admin123")
