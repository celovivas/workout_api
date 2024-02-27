from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
import sqlalchemy
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import Atleta, AtletaIn, AtletaOut, AtletaOutResumido, AtletaUpdate
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.repository.dependencies import DatabaseDependecy

router = APIRouter()





@router.get(
        path='/', 
        summary="Consultar Totos os atletas", 
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOutResumido])
async def getAllAtletas(db_session: DatabaseDependecy) -> list[AtletaOutResumido]:
    atletas: list[AtletaOutResumido] = (await db_session.execute(select(AtletaModel))).scalars().all()
    print(atletas)
    # Funcao que serializa os dados. Pega de model e converte em schema. Ela foi descontinuado. Utilizar agora o model_validate
    # return AtletaOut.from_orm()
    # neste caso, ele faz um for transformando cada atleta do atletaModel em um Atletaou (Transforma um model em um schema)
    return [AtletaOut.model_validate(atleta) for atleta in atletas]



@router.get(
        path='/filter', 
        summary="Consultar utilizando query params", 
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut])
async def getAllAtletasById(db_session: DatabaseDependecy, nome: str = "", cpf: str = "") -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel).filter(
        and_(
            AtletaModel.nome.like('%'+nome+'%'),
            AtletaModel.cpf.like('%'+cpf+'%')
            )
        ))).scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]



@router.get(
        path='/{id}', 
        summary="Consultar um atleta por Id", 
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut)
async def getAllAtletasById(id: UUID4, db_session: DatabaseDependecy) -> list[AtletaOut]:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no id: {id}")
    return atleta



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
        if isinstance(sqlalchemy.exc.IntegrityError, ex):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_model.cpf}"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro: {ex.__cause__}"
        )
    # breakpoint()
    return atleta_out
    pass


@router.patch(
        path='/{id}', 
        summary="Atualizar um atleta por Id", 
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut)
async def getAllAtletasById(id: UUID4, db_session: DatabaseDependecy, atleta_update: AtletaUpdate = Body(...)) -> AtletaOut:

    atleta_banco = await getAtletaById(db_session, id)
    # Retorna apenas os campos preenchidos
    atleta_a_ser_atualizado = atleta_update.model_dump(exclude_unset=True)
    
    for key, value in atleta_a_ser_atualizado.items():
        setattr(atleta_banco, key, value)
    
    try:
        await db_session.commit()
        await db_session.refresh(atleta_banco)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro: {ex.__cause__}"
        )
    return atleta_banco


@router.delete(
        path='/{id}', 
        summary="Deletar um atleta por Id", 
        status_code=status.HTTP_204_NO_CONTENT)
async def getAllAtletasById(id: UUID4, db_session: DatabaseDependecy) -> None:

    atleta_banco = await getAtletaById(db_session, id)
    
    try:
        await db_session.delete(atleta_banco)
        await db_session.commit()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro: {ex.__cause__}"
        )
    return atleta_banco






# Métodos de validação.
# TODO Criar classe de serviço e refatorar. Colocar regras de negócio, inclusive os métodos abaixo na classe de servico
async def verificaCPFAtleta(db_session: DatabaseDependecy, atleta_in: AtletaIn) -> AtletaModel:
    atleta: AtletaModel = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))).scalars().first()
    if atleta:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"CPF {atleta_in.cpf} já cadastrado.")
    return atleta

async def getAtletaById(db_session: DatabaseDependecy, id: UUID4) -> AtletaModel:
    atleta: AtletaModel = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Atleta com id {id} não encontrado.")
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