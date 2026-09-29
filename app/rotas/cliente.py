from app.modelos.cliente import Cliente, ClienteCriarAtualizar
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.dependencias import obter_cliente_repositorio
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from typing import Annotated

router = APIRouter(
    prefix="/api/clientes",
)

front_router = APIRouter(
    prefix="/clientes",
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_model=list[Cliente])
async def listar_clientes(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    return await cliente_repositorio.listar_clientes()


@router.get("/{cliente_id}", response_model=Cliente | None)
async def obter_cliente(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
    cliente_id: int,
):
    cliente = await cliente_repositorio.obter_cliente(cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente


@router.post("/", response_model=Cliente, status_code=201)
async def criar_cliente(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
    cliente: ClienteCriarAtualizar,
):
    return await cliente_repositorio.criar_cliente(cliente)


@router.put("/{cliente_id}", response_model=Cliente | None)
async def atualizar_cliente(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
    cliente_id: int,
    cliente: ClienteCriarAtualizar,
):
    cliente_atualizado = await cliente_repositorio.atualizar_cliente(
        cliente_id, cliente
    )
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente_atualizado


@router.delete("/{cliente_id}", status_code=204)
async def deletar_clientes(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
    cliente_id: int,
):
    sucesso = await cliente_repositorio.deletar_cliente(cliente_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")


@front_router.get("/", response_class=HTMLResponse)
async def pagina_listar_clientes(
    request: Request,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    clientes = await cliente_repositorio.listar_clientes()
    return templates.TemplateResponse(
        request,
        "clientes.html",
        {"request": request, "clientes": clientes, "titulo": "Lista de Clientes"},
    )


@front_router.get("/novo", response_class=HTMLResponse)
async def pagina_criar_cliente(request: Request):
    return templates.TemplateResponse(
        request,
        "clientes-form.html",
        {
            "request": request,
        },
    )

@front_router.get("/{cliente_id}", response_class=HTMLResponse)
async def pagina_editar_cliente(
    request: Request,
    cliente_id: int,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente = await cliente_repositorio.obter_cliente(cliente_id)
    return templates.TemplateResponse(
        request,
        "clientes-form.html",
        {
            "request": request,
            "cliente": cliente,
        },
    )
