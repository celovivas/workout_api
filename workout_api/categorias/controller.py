from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate 
from pydantic import UUID4
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from sqlalchemy.future import select

from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()

@router.get(
        path='/', 
        summary="Consultar todas as categorias", 
        status_code=status.HTTP_200_OK,
        response_model=Page[CategoriaOut])
async def getAllCategorias(db_session: DatabaseDependecy) -> Page[CategoriaOut]:
    categorias =  await paginate(db_session, select(CategoriaModel).order_by(CategoriaModel.nome))
    print(categorias)
    return categorias

#   Funcionando com o paginate default
    # print("-----------01")
    # categorias = (await db_session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))).scalars().all()
    # print("-----------02")
    # print(categorias)
    # print("-----------03")
    # return paginate(categorias)

@router.get(
        path='/{id}', 
        summary="Consultar uma categoria por Id", 
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut)
async def getAllCategoriasById(id: UUID4, db_session: DatabaseDependecy) -> list[CategoriaOut]:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id: {id}")

    print(categoria)
    return categoria


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
    # categoria_model.created_at = datetime.now()
    print(categoria_out)
    print(categoria_model.__dict__)
    print("------ chegou aqui ------")
    db_session.add(categoria_model)
    await db_session.commit()
    # breakpoint()
    # pass
    return categoria_out