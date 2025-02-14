
from fastapi import FastAPI, HTTPException
from typing import Optional

app= FastAPI(
    title='Mi primer API 196',
    description='Jose Emmanuel Morales Aguillon',
    version='1.0.1'
)

usuarios=[
    {"id":1, "nombre":"ivan", "edad": 37},
    {"id":2, "nombre":"Estrella", "edad": 21},
    {"id":3, "nombre":"Carlos", "edad": 21},
    {"id":4, "nombre":"Isacc", "edad": 21},
]

@app.get('/',tags=['Inicio'])
def main():
    return {'hola FastAPI':'JoseEmmanuel'}


#endopint Consultar todos
@app.get('/usuarios',tags=['Operaciones CRUD'])
def ConsultarTodos():
    return {"Usuarios registrados ": usuarios}

#endpoint POST
@app.post('/usuarios/',tags=['Operaciones CRUD'])
def guardar(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400,detail="El usuario ya esta registrado")

    usuarios.append(usuario)
    return usuario    

#endpoint PUT 
@app.put('/usuarios/{id}',tags=['Operaciones CRUD'])
def actualizar(id:int,usuarioActualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuarioActualizado)
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