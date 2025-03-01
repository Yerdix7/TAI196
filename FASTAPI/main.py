
from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import BearerJWT

app= FastAPI(
    title='Mi primer API 196',
    description='Jose Emmanuel Morales Aguillon',
    version='1.0.1'
)


usuarios=[
    {"id":1, "nombre":"ivan", "edad": 37, "correo":"ivan@example.com"},
    {"id":2, "nombre":"Estrella", "edad": 21, "correo":"estrella@example.com"},
    {"id":3, "nombre":"Carlos", "edad": 21, "correo":"carlos@example.com"},
    {"id":4, "nombre":"Isacc", "edad": 21, "correo":"isacc@example.com"},
]

@app.get('/',tags=['Inicio'])
def main():
    return {'hola FastAPI':'JoseEmmanuel'}


#endpoint para generar token
@app.post('/auth', tags=['Autentificacion'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'emmanuel@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.dict())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso":"Usuario no autorizado"}




#endopint Consultar todos
@app.get('/usuarios',dependencies=[Depends(BearerJWT())], response_model= List[modelUsuario], tags=['Operaciones CRUD'])
def ConsultarTodos():
    return usuarios



#endpoint para agregar usuarios
@app.post('/usuarios/', response_model=modelUsuario, tags=['Operaciones CRUD'])
def guardar(usuarionuevo: modelUsuario):
    for usr in usuarios:
        if usr["id"] == usuarionuevo.id:
            raise HTTPException(status_code=400,detail="El usuario ya esta registrado")

    usuarios.append(usuarionuevo)
    return usuarionuevo    



#endpoint actualizar usuario(PUT) 
@app.put('/usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizar_usuario(id:int, usuario_actualizado:modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]= usuario_actualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#endpoint eliminar
@app.delete('/usuarios/', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[index]
            return {"Mensaje": "Usuario eliminado con exito"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")