from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from sqlalchemy.future import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate 
from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()

@router.post(
        path='/', 
        summary="Criar novo centro de treinamento", 
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut)
async def post(
    db_session: DatabaseDependecy, 
    ct_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    # o dict está depreciado, então usaremos o model_dump, recomendado na documentacao
    # categoria_out = CategoriaOut(id=uuid4(), **categoria_in.dict())
    print("------ chegou aqui ------")
    ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
    ct_model = CentroTreinamentoModel(**ct_out.model_dump())
    print(ct_out)
    print(ct_model.__dict__)
    print("------ chegou aqui ------")
    db_session.add(ct_model)
    await db_session.commit()
    return ct_out


@router.get(
        path='/', 
        summary="Consultar todos os os centros de treinamento", 
        status_code=status.HTTP_200_OK,
        response_model=Page[CentroTreinamentoOut])
async def getAllCentrosTreinamento(db_session: DatabaseDependecy) -> Page[CentroTreinamentoOut]:
    cts =  await paginate(db_session, select(CentroTreinamentoModel).order_by(CentroTreinamentoModel.nome))
    print(cts)
    return cts


@router.get(
        path='/{id}', 
        summary="Consultar uma centro de treinamento por Id", 
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut)
async def getCentroTreinamentoById(id: UUID4, db_session: DatabaseDependecy) -> list[CentroTreinamentoOut]:
    ct: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not ct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrada no id: {id}")

    print(ct)
    return ct