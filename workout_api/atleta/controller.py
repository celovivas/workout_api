from fastapi import APIRouter, Body, status
from workout_api.atleta.schemas import Atleta, AtletaIn

from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()

@router.post(
        path='/', 
        summary="Criar novo atleta", 
        status_code=status.HTTP_201_CREATED)
async def post(
    db_session: DatabaseDependecy, 
    atleta_in: Atleta = Body(...)
):
    pass

