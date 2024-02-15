from fastapi import FastAPI

app = FastAPI(title='Workout Api - Nome da nossa app')

# Não vai precisar mais pois os parametros estão sendo setados no start da aplicação
# no comando que está no run do Makefile
# if __name__ == 'main':
#     import uvicorn

#     uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=False)

