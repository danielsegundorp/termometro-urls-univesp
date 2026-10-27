import logging
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Consulta(db.Model):
    __tablename__ = "consultas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    trust_score = db.Column(db.Integer, nullable=True)
    data_consulta = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        server_default=db.func.current_timestamp(),
    )


def init_db(app):
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            logger.exception("Não foi possível criar/verificar as tabelas no banco de dados.")


def salvar_consulta(url, trust_score):
    try:
        nova_consulta = Consulta(url=url, trust_score=trust_score)
        db.session.add(nova_consulta)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Erro ao salvar consulta no banco de dados.")


def listar_historico(limite=5):
    try:
        stmt = select(Consulta).order_by(Consulta.id.desc()).limit(limite)
        return list(db.session.scalars(stmt).all())
    except Exception:
        logger.exception("Erro ao listar histórico do banco de dados.")
        return []
