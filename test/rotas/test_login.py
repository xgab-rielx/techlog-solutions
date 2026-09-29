import pytest
from fastapi.responses import RedirectResponse

from app.modelos.usuario import Usuario
from app.rotas import login


class TestRotasLogin:
    
    @pytest.mark.asyncio
    async def test_pagina_login_retorna_template(self, mock_request):
        resultado = await login.pagina_login(mock_request)
        
        assert resultado is not None
    
    @pytest.mark.asyncio
    async def test_login_com_credenciais_validas_redireciona(
        self, mock_usuario_repositorio, mock_request
    ):
        usuario_mock = Usuario(
            id_=1,
            nome="João Silva",
            email="joao@example.com"
        )
        mock_usuario_repositorio.buscar_usuario_por_email_senha.return_value = usuario_mock
        
        resultado = await login.login(
            mock_usuario_repositorio,
            mock_request,
            email="joao@example.com",
            senha="senha123"
        )
        
        assert isinstance(resultado, RedirectResponse)
        assert resultado.status_code == 303
        assert resultado.headers["location"] == "/"
        # Verifica se o cookie de sessão foi definido
        assert "session_token" in resultado.headers.get("set-cookie", "")
        
        mock_usuario_repositorio.buscar_usuario_por_email_senha.assert_called_once_with(
            "joao@example.com",
            "senha123"
        )
    
    @pytest.mark.asyncio
    async def test_login_com_credenciais_invalidas_retorna_erro(
        self, mock_usuario_repositorio, mock_request
    ):       
        mock_usuario_repositorio.buscar_usuario_por_email_senha.return_value = None
        
        resultado = await login.login(
            mock_usuario_repositorio,
            mock_request,
            email="joao@example.com",
            senha="senha_errada"
        )
        
        # O resultado não é um RedirectResponse quando há erro
        assert not isinstance(resultado, RedirectResponse)
        mock_usuario_repositorio.buscar_usuario_por_email_senha.assert_called_once_with(
            "joao@example.com",
            "senha_errada"
        )
    
    @pytest.mark.asyncio
    async def test_login_com_email_inexistente(
        self, mock_usuario_repositorio, mock_request
    ):       
        mock_usuario_repositorio.buscar_usuario_por_email_senha.return_value = None
        
        resultado = await login.login(
            mock_usuario_repositorio,
            mock_request,
            email="naoexiste@example.com",
            senha="senha123"
        )
        
        assert not isinstance(resultado, RedirectResponse)
        mock_usuario_repositorio.buscar_usuario_por_email_senha.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_define_cookie_httponly(
        self, mock_usuario_repositorio, mock_request
    ):       
        usuario_mock = Usuario(
            id_=1,
            nome="João Silva",
            email="joao@example.com"
        )
        mock_usuario_repositorio.buscar_usuario_por_email_senha.return_value = usuario_mock
        
        resultado = await login.login(
            mock_usuario_repositorio,
            mock_request,
            email="joao@example.com",
            senha="senha123"
        )
        
        # Verifica se o cookie tem a flag httponly
        set_cookie_header = resultado.headers.get("set-cookie", "")
        assert "httponly" in set_cookie_header.lower()
    
    @pytest.mark.asyncio
    async def test_login_sucesso_usa_token_fixo(
        self, mock_usuario_repositorio, mock_request
    ):
        usuario_mock = Usuario(
            id_=1,
            nome="João Silva",
            email="joao@example.com"
        )
        mock_usuario_repositorio.buscar_usuario_por_email_senha.return_value = usuario_mock
        
        resultado = await login.login(
            mock_usuario_repositorio,
            mock_request,
            email="joao@example.com",
            senha="senha123"
        )
        
        # Verifica que o token atual é fixo
        set_cookie_header = resultado.headers.get("set-cookie", "")
        assert "session_token=token-senha" in set_cookie_header