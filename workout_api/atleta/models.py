from datetime import datetime
from workout_api.contrib.models import BaseModel
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AtletaModel(BaseModel):
    __tablename__ = "atleta"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=True)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=True)
    idade: Mapped[str] = mapped_column(Integer, nullable=False)
    peso: Mapped[str] = mapped_column(Float, nullable=False)
    altura: Mapped[str] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atleta', lazy="selectin")
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categoria.pk_id'))

    # Atributos com o mesmo nome do banco
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atleta', lazy="selectin")
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centro_treinamento.pk_id'))