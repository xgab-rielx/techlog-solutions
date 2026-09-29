from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from typing import Annotated

from app.dependencias import obter_usuario_repositorio
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio

router = APIRouter(
    prefix="/login",
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})



@router.post("/", response_class=HTMLResponse)
async def login(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    request: Request, 
    email = Form(...), 
    senha = Form(...), 
    ):

    usuario = await usuario_repositorio.buscar_usuario_por_email_senha(email, senha)
    if usuario:
        response =  RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)

        return response

    return templates.TemplateResponse(request, "login.html", {
        "request": request,
        "email": email,
        "senha": senha,
        "error": "Email ou senha inválidos"
    })
        