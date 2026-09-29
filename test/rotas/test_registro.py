import pytest
from fastapi.responses import RedirectResponse

from app.rotas import registro
from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


class TestRotasRegistro:
    
    @pytest.mark.asyncio
    async def test_pagina_registro_retorna_template(self, mock_request):
        resultado = await registro.pagina_registro(mock_request)
        
        assert resultado is not None
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_com_dados_validos_sucesso(
        self, mock_usuario_repositorio, mock_request
    ):        
        mock_usuario_repositorio.buscar_usuario_por_email.return_value = None
        usuario_criado = Usuario(
            id_=1,
            nome="João Silva",
            email="joao@example.com"
        )
        mock_usuario_repositorio.criar_usuario.return_value = usuario_criado
        
        resultado = await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="João Silva",
            email="joao@example.com",
            senha="senha123",
            confirma_senha="senha123"
        )
        
        assert isinstance(resultado, RedirectResponse)
        assert resultado.status_code == 303
        assert resultado.headers["location"] == "/login"
        
        mock_usuario_repositorio.buscar_usuario_por_email.assert_called_once_with(
            "joao@example.com"
        )
        mock_usuario_repositorio.criar_usuario.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_com_email_existente_retorna_erro(
        self, mock_usuario_repositorio, mock_request
    ):        
        usuario_existente = Usuario(
            id_=1,
            nome="João Existente",
            email="joao@example.com"
        )
        mock_usuario_repositorio.buscar_usuario_por_email.return_value = usuario_existente
        
        resultado = await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="João Silva",
            email="joao@example.com",
            senha="senha123",
            confirma_senha="senha123"
        )
        
        assert not isinstance(resultado, RedirectResponse)
        mock_usuario_repositorio.buscar_usuario_por_email.assert_called_once_with(
            "joao@example.com"
        )
        # Não deve tentar criar o usuário
        mock_usuario_repositorio.criar_usuario.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_com_campo_vazio_retorna_erro(
        self, mock_usuario_repositorio, mock_request
    ):       
        resultado = await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="",
            email="joao@example.com",
            senha="senha123",
            confirma_senha="senha123"
        )
        
        assert not isinstance(resultado, RedirectResponse)
        # Não deve chamar o repositório se os campos são inválidos
        mock_usuario_repositorio.buscar_usuario_por_email.assert_not_called()
        mock_usuario_repositorio.criar_usuario.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_cria_objeto_correto(
        self, mock_usuario_repositorio, mock_request
    ):        
        mock_usuario_repositorio.buscar_usuario_por_email.return_value = None
        usuario_criado = Usuario(
            id_=1,
            nome="Maria Santos",
            email="maria@example.com"
        )
        mock_usuario_repositorio.criar_usuario.return_value = usuario_criado
        
        await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="Maria Santos",
            email="maria@example.com",
            senha="senhaSegura123",
            confirma_senha="senhaSegura123"
        )
        
        # Verifica que criar_usuario foi chamado com o objeto correto
        call_args = mock_usuario_repositorio.criar_usuario.call_args
        usuario_criar = call_args[0][0]
        
        assert isinstance(usuario_criar, UsuarioCriarAtualizar)
        assert usuario_criar.nome == "Maria Santos"
        assert usuario_criar.email == "maria@example.com"
        assert usuario_criar.senha == "senhaSegura123"
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_falha_na_criacao_retorna_erro(
        self, mock_usuario_repositorio, mock_request
    ):        
        mock_usuario_repositorio.buscar_usuario_por_email.return_value = None
        mock_usuario_repositorio.criar_usuario.return_value = None
        
        resultado = await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="João Silva",
            email="joao@example.com",
            senha="senha123",
            confirma_senha="senha123"
        )
        
        assert not isinstance(resultado, RedirectResponse)
    
    @pytest.mark.asyncio
    async def test_registrar_usuario_redireciona_para_login_apos_sucesso(
        self, mock_usuario_repositorio, mock_request
    ):       
        mock_usuario_repositorio.buscar_usuario_por_email.return_value = None
        usuario_criado = Usuario(
            id_=1,
            nome="João Silva",
            email="joao@example.com"
        )
        mock_usuario_repositorio.criar_usuario.return_value = usuario_criado
        
        resultado = await registro.registrar_usuario(
            mock_usuario_repositorio,
            mock_request,
            nome="João Silva",
            email="joao@example.com",
            senha="senha123",
            confirma_senha="senha123"
        )
        
        assert isinstance(resultado, RedirectResponse)
        assert resultado.headers["location"] == "/login"