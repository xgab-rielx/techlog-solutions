import pytest
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


@pytest.fixture
def usuario_repositorio(mock_banco_dados):
    return UsuarioRepositorio(mock_banco_dados)


class TestUsuarioRepositorio:
    
    @pytest.mark.asyncio
    async def test_buscar_usuario_por_email_senha_sucesso(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = (1, "João Silva", "joao@example.com")
        
        resultado = await usuario_repositorio.buscar_usuario_por_email_senha(
            "joao@example.com", 
            "senha123"
        )
        
        assert resultado is not None
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@example.com"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email FROM usuarios WHERE email = ? AND senha = ?",
            ("joao@example.com", "senha123")
        )
    
    @pytest.mark.asyncio
    async def test_buscar_usuario_por_email_senha_credenciais_invalidas(
        self, usuario_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = None
        
        resultado = await usuario_repositorio.buscar_usuario_por_email_senha(
            "joao@example.com",
            "senha_errada"
        )
        
        assert resultado is None
    
    @pytest.mark.asyncio
    async def test_buscar_usuario_por_email_existente(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = (1, "João Silva", "joao@example.com")
        
        resultado = await usuario_repositorio.buscar_usuario_por_email("joao@example.com")
        
        assert resultado is not None
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@example.com"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email FROM usuarios WHERE email = ?",
            ("joao@example.com",)
        )
    
    @pytest.mark.asyncio
    async def test_buscar_usuario_por_email_inexistente(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = None
        
        resultado = await usuario_repositorio.buscar_usuario_por_email("naoexiste@example.com")
        
        assert resultado is None
    
    @pytest.mark.asyncio
    async def test_criar_usuario_sucesso(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.lastrowid = 1
        
        usuario_criar = UsuarioCriarAtualizar(
            nome="João Silva",
            email="joao@example.com",
            senha="senha123"
        )
        
        resultado = await usuario_repositorio.criar_usuario(usuario_criar)
        
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@example.com"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            ("João Silva", "joao@example.com", "senha123")
        )
    
    @pytest.mark.asyncio
    async def test_criar_usuario_com_dados_validos(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.lastrowid = 2
        
        usuario_criar = UsuarioCriarAtualizar(
            nome="Maria Santos",
            email="maria@example.com",
            senha="senhaSegura456"
        )
        
        resultado = await usuario_repositorio.criar_usuario(usuario_criar)
        
        assert resultado.id_ == 2
        assert resultado.nome == "Maria Santos"
        assert resultado.email == "maria@example.com"
    
    @pytest.mark.asyncio
    async def test_buscar_usuario_verifica_email_correto(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = None
        
        email_busca = "teste@example.com"
        await usuario_repositorio.buscar_usuario_por_email(email_busca)
        
        call_args = mock_banco_dados.cursor.execute.call_args
        assert call_args[0][1] == (email_busca,)