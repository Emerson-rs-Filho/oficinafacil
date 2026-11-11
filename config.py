import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _url_banco():
    """Usa DATABASE_URL se existir (ex.: PostgreSQL do Supabase); senão, SQLite local."""
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        return "sqlite:///" + os.path.join(BASE_DIR, "oficinafacil.db")
    # O Supabase fornece "postgres://" ou "postgresql://"; usamos o driver psycopg (v3)
    for prefixo in ("postgres://", "postgresql://"):
        if url.startswith(prefixo):
            url = "postgresql+psycopg://" + url[len(prefixo):]
    return url


class Config:
    """Configurações da aplicação.

    - Local: SQLite (arquivo oficinafacil.db), sem configurar nada.
    - Produção (Render + Supabase): defina DATABASE_URL e SECRET_KEY.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    SQLALCHEMY_DATABASE_URI = _url_banco()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Testa a conexão antes de usar (evita erro após o banco ficar ocioso)
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
