from fastapi import FastAPI
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

@app.get('/promedio',tags=['Mi calificacion TAI'])
def promedio():
    return 7.99998

#endpoint Parametro obligatorio
@app.get('/usuario/{id}',tags=['Parametro Obligatorio'])
def consultaUsuario(id:int):
    #Conectamos BD
    #Hacemos consultas y retornamos resultados7
    return{"Se encontro el usuario":id}

#endpoint Parametro obligatorio
@app.get('/usuariox/{id}',tags=['Parametro Opcional'])
def consultaUsuario2(id :Optional[int]= None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":f"No se encontro el id: id"}
    else:
        return{"mensaje": "No se proporciono un Id"}            

#endpoint con varios parametro opcionales
@app.get('/usuariosa/{id}', tags=['3 parámetros opcionales'])
def consulta_usuarios3(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["usuario_id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}