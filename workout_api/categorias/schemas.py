from workout_api.contrib.schemas import BaseSchema, OutMixin
from pydantic import UUID4, Field
from typing import Annotated


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description='Nnome da categoria', example='Scale', max_length=50)]


class CategoriaIn(Categoria):
    pass


class CategoriaOut(Categoria):
     id: Annotated[UUID4, Field(description="Identificador da categoria", example="a771f162-627c-48c3-8900-1da8d8323d99")]