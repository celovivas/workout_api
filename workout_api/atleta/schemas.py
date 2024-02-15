from typing import Annotated
from pydantic import BaseModel, Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nnome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='11122233221', max_length=11)]
    idade: Annotated[int, Field(description='CPF do atleta', example=25, max_digits=3)
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=67.5, max=300)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75, max=3)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]