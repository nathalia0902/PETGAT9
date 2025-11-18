from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    cpf: str
    funcao: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str