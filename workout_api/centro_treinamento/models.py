from datetime import datetime
from workout_api.contrib.models import BaseModel
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CentroTreinamentoModel(BaseModel):
    __tablename__ = "centro_treinamento"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String[60], nullable=False)
    proprietario: Mapped[str] = mapped_column(String[30], nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    atleta: Mapped['AtletaModel'] = relationship(back_populates='centro_treinamento')
    # proprietario: Mapped[str] = mapped_column(String[30], nullable=False)
    # proprietario: Mapped['AtletaModel'] = relationship(back_populates='centro_treinamento')