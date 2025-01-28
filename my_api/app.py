from fastapi import FastAPI

from my_api.modules.auth.auth import auth_router
from my_api.modules.investments.investments import router as investments_router
from my_api.modules.tibia.tibia import router as tibia_router
from my_api.modules.users.users import user_router

contact = {
    'name': 'Gilmar',
    'email': 'gilmar.neo@gmail.com',
    'cel': '+5581995280048',
    'country': 'Brazil',
    'city': 'Jaboatão dos Guararapes',
    'state': 'Pernambuco',
    'role': 'Fullstack Developer',
    'github': '@g42puts'
}

app = FastAPI(
    contact=contact,
    description='API com rotas customizadas com diversas utilidades',
    docs_url='/docs',
    title='FastAPI de Gilmar',
    version='0.0.1',
    root_path='/api/v1',
)

app.include_router(auth_router)
app.include_router(tibia_router)
app.include_router(investments_router)
app.include_router(user_router)


@app.on_event('startup')
def on_startup():
    print('API Started', app.title, app.description, app.docs_url)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}
