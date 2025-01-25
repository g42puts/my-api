from fastapi import FastAPI

from my_api.routes.investments import investments
from my_api.routes.tibia import tibia

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

app.include_router(tibia.router)
app.include_router(investments.router)


@app.on_event('startup')
def on_startup():
    print('API Started', app.title, app.description, app.docs_url)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}
