from uuid import uuid4
from fastapi import APIRouter, Body, status
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut

from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()

@router.post(
        path='/', 
        summary="Criar nova categoria", 
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut)
async def post(
    db_session: DatabaseDependecy, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    
    # o dict está depreciado, então usaremos o model_dump, recomendado na documentacao
    # categoria_out = CategoriaOut(id=uuid4(), **categoria_in.dict())
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    print(categoria_out)
    # breakpoint()
    # pass
    return categoria_out

