# workout_api
--------------------------------------------------------
workout_api - Api usando python e fastAPI
--------------------------------------------------------
API em Python para uma competição de crossfit. Cadastro de atletas, categorias e centro de treinamento
Aplicação criada para fins de estudos a partir do curso da DIO.

Ferramentas utilizadas:
alembic==1.13.1
annotated-types==0.6.0
anyio==4.2.0
async-timeout==4.0.3
asyncpg==0.29.0
click==8.1.7
fastapi==0.109.2
fastapi-pagination==0.12.17
greenlet==3.0.3
h11==0.14.0
idna==3.6
Mako==1.3.2
MarkupSafe==2.1.5
pydantic==2.6.1
pydantic-settings==2.2.1
pydantic_core==2.16.2
python-dotenv==1.0.1
sniffio==1.3.0
SQLAlchemy==2.0.25
starlette==0.36.3
typing_extensions==4.9.0
uvicorn==0.27.0.post1


Abaixo diversos referências e comandos utilizados para instalação, configuração da aplicação, 
assim como para rodar a mesma.

--------------------------------------------------------
Passo a passo para rodar a aplicação
--------------------------------------------------------


- Criar ambiente de trabalho
pyenv virtualenv 3.11.4 workoutapi

- listar todos os ambientes criados
pyenv virtualenvs

- Ativar / acessar ambiente de trablaho
pyenv activate workoutapi 

- instalar bibliotecas que iremos utilizar
pip install fastapi uvicorn sqlalchemy pydantic

- Para subir o docker
docer compose up -d

- Instalar o alembic
pip install alembic

- para iniciar o alembic
alembic init alembic

- Instalar o aysncpg 
pip install asyncpg


- Instalar settings do pydantic
pip install pydantic.settings
pip install pydantic-settings

-Instalar fastapi-pagination
pip install fastapi-pagination


--- Comandos para nossa app que estão cadastrados no makeFile
----------------------------------------------------------------

- Rodar a aplicação
make run

- Criar os arquivos de migração
make create-migrations d="init_db"

- Rodar as migrations
run-migrations



Após subir a aplicação, acessar pelo swagger:
http://localhost:8000/docs




--------------------------------------------------------
Passo a passo durante o desenvolvimento
--------------------------------------------------------
Instalando o pyenv e exemplo de como usar
https://medium.com/@aashari/easy-to-follow-guide-of-how-to-install-pyenv-on-ubuntu-a3730af8d7f0


- Instalar o pyenv 3,11.4
pyenv install 3.11.4

- listar todos os ambientes criados
pyenv virtualenvs

- remover um ambiente e todas as versões instaladas 
pyenv uninstall 3.11.4/envs/workoutapi
ou
- Remover apenas o ambiente virtual
pyenv virtualenv-delete <venv-name>


Comandos para o projeto workoutapi
--------------------------------------------------

Referencias
FastAPI: https://fastapi.tiangolo.com/reference/fastapi/
uvicorn: https://www.uvicorn.org/
Pydantic: https://docs.pydantic.dev/latest/
Sql Alchemy: https://docs.sqlalchemy.org/en/20/
Alembic: https://alembic.sqlalchemy.org/en/latest/
fastapi-pagination: https://uriyyo-fastapi-pagination.netlify.app/




- Criar ambiente de trabalho
pyenv virtualenv 3.11.4 workoutapi

- listar todos os ambientes criados
pyenv virtualenvs

- Ativar / acessar ambiente de trablaho
pyenv activate workoutapi 


- instalar bibliotecas que iremos utilizar
pip install fastapi uvicorn sqlalchemy pydantic


- Para configurar o interpretador do ambiente que estaremos utilizando seguir o passo a passo
1- Instalar a extensão Python no vs code
2- ctrl+shif+p e digitar: Python: Select Interpreter
3- Selecionar o ambiente virtual que iremos utilizar


- Para subir o servidor:
uvicorn workout_api.main:app --reload

- Após criar o arquivo Makefile, conseguimos dar comandos curtos mapeando para os comandos reais.
Ex.: Basta no terminal, digitar: 'make run' e ele irá executar o comando que está logo abaixo associado a ele


- Para subir o docker
docer compose up -d

- Instalar o alembic
pip install alembic

- para iniciar o alembic
alembic init alembic

- Criar aquivo requirements.txt que contém todas as configurações de versões de bibliotecas que estamos utilizando
pip freeze > requirements.txt


- Instalar o aysncpg para utilizarmos funções assúncronaas. Para banco de dados, reparar na url do driver do banco onde utilizamos ele
pip install asyncpg



- Instalar settings do pydantic
pip install pydantic.settings
pip install pydantic-settings


---Incluir a paginação
--------------------------------------
https://uriyyo-fastapi-pagination.netlify.app/

-Instalar fastapi-pagination
pip install fastapi-pagination


--- Comandos para nossa app que estão cadastrados no makeFile
-------------------------------------------------------------------------------------------------

- Rodar a aplicação
make run

- Criar os arquivos de migração
make create-migrations d="init_db"

- Rodar as migrations
run-migrations
