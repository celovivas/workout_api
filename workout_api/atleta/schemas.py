from typing import Annotated, Optional
from pydantic import BaseModel, Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nnome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='11122233221', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25, ge=1,le=200)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=95.5, ge=20, le=200)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75, ge=0.5, le=3.0)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nnome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[Optional[str], Field(None, description='CPF do atleta', example='11122233221', max_length=11)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25, ge=1,le=200)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description='Altura do atleta', example=1.75, ge=0.5, le=3.0)]


class AtletaOutResumido(BaseSchema):
    nome: Annotated[str, Field( description='Nnome do atleta', example='Joao', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]