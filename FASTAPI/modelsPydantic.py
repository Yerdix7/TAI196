
from pydantic import BaseModel,Field,EmailStr

#modelo para validacion de datos
class modelUsuario(BaseModel):
    id:int = Field(...,gt=0, description="Id unico y numeros positivos")
    nombre:str = Field(..., min_length=3 ,max_length=15, description="Nombre debe contener solo letras y espacios ")
    edad: int = Field(..., gt=0, lt=130, description="Edad debe ser un número positivo entre 1 y 130")
    correo: EmailStr = Field(..., description="Correo electrónico válido")