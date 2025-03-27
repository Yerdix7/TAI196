
from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import BearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User

app= FastAPI(
    title='Mi primer API 196',
    description='Jose Emmanuel Morales Aguillon',
    version='1.0.1'
)
#levanta las tablas definidas en modelos 
Base.metadata.create_all(bind=engine)


@app.get('/',tags=['Inicio'])
def main():
    return {'hola FastAPI':'JoseEmmanuel'}


#endopint Consultar todos
@app.get('/usuarios', tags=['Operaciones CRUD'])
def ConsultarTodos():
    db= Session()
    try:
        consulta= db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))

    except Exception as x:
        return JSONResponse(status_code=500,
                         content={'mensaje':"No fue posible consultar",
                                     "Excepcion": str(x) })

    finally:
        db.close()





#endopint Consulta por id
@app.get('/usuario/{id}', tags=['Operaciones CRUD'])
def ConsultarUno(id:int):
    db= Session()
    try:
        consulta= db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code= 404,content={"Mensaje":"Usuario no enconteado"})
        
        return JSONResponse(content=jsonable_encoder(consulta))

    except Exception as x:
        return JSONResponse(status_code=500,
                         content={'mensaje':"No fue posible consultar",
                                     "Excepcion": str(x) })

    finally:
        db.close()




#endpoint para agregar usuarios
@app.post('/usuarios/', response_model=modelUsuario, tags=['Operaciones CRUD'])
def AgregarUsuario(usuarionuevo: modelUsuario):
    db= Session()
    try:
        db.add(User(**usuarionuevo.dict() ))
        db.commit()
        return JSONResponse(status_code=201,
                            content={'mensaje':"Usuario Guardado",
                                     "usuario": usuarionuevo.dict() })

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={'mensaje':"No se guardo",
                                     "Excepcion": str(e) })


    finally:
        db.close()




""" #endpoint actualizar usuario(PUT) 
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
    raise HTTPException(status_code=404, detail="Usuario no encontrado") """

#endpoint para generar token
@app.post('/auth', tags=['Autentificacion'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'emmanuel@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.dict())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso":"Usuario no autorizado"}