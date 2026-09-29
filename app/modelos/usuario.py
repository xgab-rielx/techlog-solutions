from pydantic import BaseModel

class Usuario(BaseModel):
    id_: int 
    nome: str
    email: str
    senha: str | None = None

class UsuarioCriarAtualizar(BaseModel):
    nome: str
    email: str
    senha: str | None = None