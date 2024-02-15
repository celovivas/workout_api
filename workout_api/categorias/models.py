from datetime import datetime
from workout_api.contrib.models import BaseModel
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CategoriaModel(BaseModel):
    __tablename__ = "categoria"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')