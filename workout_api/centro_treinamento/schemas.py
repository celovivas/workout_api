from workout_api.contrib.schemas import BaseSchema
from pydantic import Field
from typing import Annotated


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Av. Luiz Feijão, 43', max_length=60)]
    proprietaro: Annotated[str, Field(description='Nome do proprietário', example='Joaquim José', max_length=30)]