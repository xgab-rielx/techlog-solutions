from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from typing import Annotated

from app.dependencias import obter_usuario_repositorio
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.modelos.usuario import UsuarioCriarAtualizar

router = APIRouter(
    prefix="/registro",
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request, "registro.html", {"request": request})

@router.post("/")
async def registrar_usuario(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    request: Request,
    nome = Form(...),
    email = Form(...),
    senha = Form(...),
    confirma_senha = Form(...),
):  
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha
    }

    if not all([nome, email, senha, confirma_senha]):
        return templates.TemplateResponse(request, "registro.html", {
            "request": request,
            "error": "Campos obrigatórios não preenchidos",
            **data
        })

    if senha != confirma_senha:
        return templates.TemplateResponse(request, "registro.html", {
            "request": request,
            "error": "As senhas não conferem",
            **data
        })

    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)
    if usuario_existente:
        return templates.TemplateResponse(request, "registro.html", {
            "request": request,
            "error": "Usuário invalido!",
            **data
        })

    usuario_criar = UsuarioCriarAtualizar(nome=nome, email=email, senha=senha)
    usuario = await usuario_repositorio.criar_usuario(usuario_criar)

    if usuario:
        response = RedirectResponse(url="/login", status_code=303)
        return response

    return templates.TemplateResponse(request, "registro.html", {
                "request": request,
                "error": "Não foi possivel criar o usuário. Tente novamente.",
                **data
            })