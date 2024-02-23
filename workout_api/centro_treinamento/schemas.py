from workout_api.contrib.schemas import BaseSchema
from pydantic import UUID4, Field
from typing import Annotated


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Av. Luiz Feijão, 43', max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do proprietário', example='Joaquim José', max_length=30)]


class CentroTreinamentoAtleta(CentroTreinamento):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]


class CentroTreinamentoIn(CentroTreinamento):
    pass


class CentroTreinamentoOut(CentroTreinamento):
     id: Annotated[UUID4, Field(description="Identificador do centro de treinamento", example="a771f162-627c-48c3-8900-1da8d8323d99")]