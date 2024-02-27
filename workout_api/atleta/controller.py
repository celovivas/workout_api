from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import Atleta, AtletaIn, AtletaOut
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()


@router.post(
        path='/', 
        summary="Criar novo atleta", 
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut)
async def post(
    db_session: DatabaseDependecy, 
    atleta_in: AtletaIn = Body(...)
) -> AtletaOut:

    # Verifica se existe a categoria
    categoria: CategoriaModel = await getCategoria(db_session, atleta_in)

    # Verifica se existe o centro de treinamento
    centro_treinamento: CentroTreinamentoModel = await getCentroTreinamento(db_session, atleta_in)

    atleta_ja_cadastrado = await verificaCPFAtleta(db_session, atleta_in)

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    
    # NÃO MAPEAR o objeto inteiro. Fiz deste jeito, ele salva 1 vez mas não salva nas outras.
    # atleta_model.categoria = categoria
    # atleta_model.centro_treinamento = centro_treinamento
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
    try:
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro: {ex.__cause__}"
        )
    # breakpoint()
    return atleta_out
    pass


async def verificaCPFAtleta(db_session: DatabaseDependecy, atleta_in: AtletaIn) -> CategoriaModel:
    atleta: AtletaModel = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))).scalars().first()
    if atleta:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"CPF {atleta_in.cpf} já cadastrado.")
    return atleta

async def getCategoria(db_session: DatabaseDependecy, atleta_in: AtletaIn) -> CategoriaModel:
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Categoria {atleta_in.categoria.nome} não encontrada.")
    print(f"categoria -->  {categoria.__dict__}")
    return categoria

async def getCentroTreinamento(db_session: DatabaseDependecy, atleta_in: AtletaIn) -> CentroTreinamentoModel:
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Centro de Treinamento {atleta_in.centro_treinamento.nome} não encontrado.")
    print(f"Centro de Treinamento -->  {centro_treinamento.__dict__}")
    return centro_treinamento


@router.get(
        path='/', 
        summary="Consultar Totos os atletas", 
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut])
async def getAllAtletas(db_session: DatabaseDependecy) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    print(atletas)
    return atletas

# @router.get(
#         path='/{id}', 
#         summary="Consultar uma categoria por Id", 
#         status_code=status.HTTP_200_OK,
#         response_model=CategoriaOut)
# async def getAllCategoriasById(id: UUID4, db_session: DatabaseDependecy) -> list[CategoriaOut]:
#     categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

#     if not categoria:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id: {id}")

#     print(categoria)
#     return categoria