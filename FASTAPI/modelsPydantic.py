
from pydantic import BaseModel,Field,EmailStr

#modelo para validacion de datos
class modelUsuario(BaseModel):
    name:str = Field(..., min_length=3 ,max_length=50, description="Nombre debe contener solo letras y espacios ")
    age: int = Field(..., gt=0, lt=130, description="Edad debe ser un número positivo entre 1 y 130")
    email: EmailStr = Field(..., description="Correo electrónico válido")

class modelAuth(BaseModel):
    correo:EmailStr
    passw:str = Field(..., min_length=8,strip_whitespace=True, description="Contraseña minimo 8 caracteres")