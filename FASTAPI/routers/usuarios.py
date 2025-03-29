from fastapi import HTTPException,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modelUsuario
from middlewares import BearerJWT
from DB.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter

routerUsuario= APIRouter()

#dependencies=[Depends(BearerJWT())]

#endopint Consultar todos
@routerUsuario.get('/usuarios', tags=['Operaciones CRUD'])
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
@routerUsuario.get('/usuario/{id}', tags=['Operaciones CRUD'])
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
@routerUsuario.post('/usuarios/', response_model=modelUsuario, tags=['Operaciones CRUD'])
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


# Endpoint para actualizar usuario
@routerUsuario.put('/usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"Mensaje": "Usuario no encontrado"})
        
        for key, value in usuario_actualizado.dict().items():
            setattr(usuario, key, value)
        
        db.commit()
        return JSONResponse(content=jsonable_encoder(usuario))
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "No se pudo actualizar el usuario", "Excepcion": str(e)})
    finally:
        db.close()

# Endpoint para eliminar usuario
@routerUsuario.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"Mensaje": "Usuario no encontrado"})
        
        db.delete(usuario)
        db.commit()
        return JSONResponse(content={"Mensaje": "Usuario eliminado con éxito"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "No se pudo eliminar el usuario", "Excepcion": str(e)})
    finally:
        db.close()