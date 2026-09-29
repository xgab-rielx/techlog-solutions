import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from app.modelos.cliente import Cliente, ClienteCriarAtualizar
from app.rotas import cliente

class TestRotasClienteAPI:
    
    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_vazia(self, mock_cliente_repositorio):       
        mock_cliente_repositorio.listar_clientes.return_value = []
        
        resultado = await cliente.listar_clientes(mock_cliente_repositorio)
        
        assert resultado == []
        mock_cliente_repositorio.listar_clientes.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_com_clientes(self, mock_cliente_repositorio):
        clientes_mock = [
            Cliente(id_=1, nome="João", email="joao@example.com", telefone="11999999999"),
            Cliente(id_=2, nome="Maria", email="maria@example.com", telefone="11888888888")
        ]
        mock_cliente_repositorio.listar_clientes.return_value = clientes_mock
        
        resultado = await cliente.listar_clientes(mock_cliente_repositorio)
        
        assert len(resultado) == 2
        assert resultado[0].nome == "João"
        assert resultado[1].nome == "Maria"
    
    @pytest.mark.asyncio
    async def test_obter_cliente_existente(self, mock_cliente_repositorio):        
        cliente_mock = Cliente(
            id_=1,
            nome="João",
            email="joao@example.com",
            telefone="11999999999"
        )
        mock_cliente_repositorio.obter_cliente.return_value = cliente_mock
        
        resultado = await cliente.obter_cliente(mock_cliente_repositorio, 1)
        
        assert resultado.id_ == 1
        assert resultado.nome == "João"
        mock_cliente_repositorio.obter_cliente.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_obter_cliente_inexistente_lanca_excecao(self, mock_cliente_repositorio):
        mock_cliente_repositorio.obter_cliente.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await cliente.obter_cliente(mock_cliente_repositorio, 999)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente não encontrado!"
    
    @pytest.mark.asyncio
    async def test_criar_cliente_sucesso(self, mock_cliente_repositorio):
        cliente_criar = ClienteCriarAtualizar(
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        cliente_criado = Cliente(
            id_=1,
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        mock_cliente_repositorio.criar_cliente.return_value = cliente_criado
        
        resultado = await cliente.criar_cliente(mock_cliente_repositorio, cliente_criar)
        
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        mock_cliente_repositorio.criar_cliente.assert_called_once_with(cliente_criar)
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_existente(self, mock_cliente_repositorio):
        cliente_atualizar = ClienteCriarAtualizar(
            nome="João Silva Atualizado",
            email="joao.novo@example.com",
            telefone="11777777777"
        )
        cliente_atualizado = Cliente(
            id_=1,
            nome="João Silva Atualizado",
            email="joao.novo@example.com",
            telefone="11777777777"
        )
        mock_cliente_repositorio.atualizar_cliente.return_value = cliente_atualizado
        
        resultado = await cliente.atualizar_cliente(mock_cliente_repositorio, 1, cliente_atualizar)
        
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva Atualizado"
        mock_cliente_repositorio.atualizar_cliente.assert_called_once_with(1, cliente_atualizar)
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_inexistente_lanca_excecao(self, mock_cliente_repositorio):
        cliente_atualizar = ClienteCriarAtualizar(
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        mock_cliente_repositorio.atualizar_cliente.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await cliente.atualizar_cliente(mock_cliente_repositorio, 999, cliente_atualizar)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente não encontrado!"
    
    @pytest.mark.asyncio
    async def test_deletar_cliente_existente(self, mock_cliente_repositorio):
        mock_cliente_repositorio.deletar_cliente.return_value = True
        
        resultado = await cliente.deletar_cliente(mock_cliente_repositorio, 1)
        
        assert resultado is None
        mock_cliente_repositorio.deletar_cliente.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_deletar_cliente_inexistente_lanca_excecao(self, mock_cliente_repositorio):
        mock_cliente_repositorio.deletar_cliente.return_value = False
        
        with pytest.raises(HTTPException) as exc_info:
            await cliente.deletar_cliente(mock_cliente_repositorio, 999)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente não encontrado!"


class TestRotasClienteFrontend:
    
    @pytest.mark.asyncio
    async def test_pagina_listar_clientes_retorna_template(self, mock_cliente_repositorio, mock_request):
        clientes_mock = [
            Cliente(id_=1, nome="João", email="joao@example.com", telefone="11999999999")
        ]
        mock_cliente_repositorio.listar_clientes.return_value = clientes_mock
        
        resultado = await cliente.pagina_listar_clientes(mock_request, mock_cliente_repositorio)
        
        assert resultado is not None
        mock_cliente_repositorio.listar_clientes.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_pagina_criar_cliente_retorna_formulario(self, mock_request):        
        resultado = await cliente.pagina_criar_cliente(mock_request)
        
        assert resultado is not None
    
    @pytest.mark.asyncio
    async def test_pagina_editar_cliente_retorna_formulario(self, mock_cliente_repositorio, mock_request):
        cliente_mock = Cliente(
            id_=1,
            nome="João",
            email="joao@example.com",
            telefone="11999999999"
        )
        mock_cliente_repositorio.obter_cliente.return_value = cliente_mock
        
        resultado = await cliente.pagina_editar_cliente(mock_request, 1, mock_cliente_repositorio)
        
        assert resultado is not None
        mock_cliente_repositorio.obter_cliente.assert_called_once_with(1)