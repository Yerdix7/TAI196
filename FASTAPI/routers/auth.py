
from fastapi.responses import JSONResponse
from modelsPydantic import modelAuth
from tokenGen import createToken
from fastapi import APIRouter

routerAuth= APIRouter()

#endpoint para generar token
@routerAuth.post('/auth', tags=['Autentificacion'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'emmanuel@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.dict())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso":"Usuario no autorizado"}