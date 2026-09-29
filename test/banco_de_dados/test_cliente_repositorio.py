import pytest
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.modelos.cliente import ClienteCriarAtualizar


@pytest.fixture
def cliente_repositorio(mock_banco_dados):
    return ClienteRepositorio(mock_banco_dados)


class TestClienteRepositorio:
    
    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_vazia(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchall.return_value = []
        
        resultado = await cliente_repositorio.listar_clientes()
        
        assert resultado == []
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email, telefone FROM clientes"
        )
    
    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_com_clientes(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchall.return_value = [
            (1, "João Silva", "joao@example.com", "11999999999"),
            (2, "Maria Santos", "maria@example.com", "11888888888")
        ]
        
        resultado = await cliente_repositorio.listar_clientes()
        
        assert len(resultado) == 2
        assert resultado[0].id_ == 1
        assert resultado[0].nome == "João Silva"
        assert resultado[0].email == "joao@example.com"
        assert resultado[1].id_ == 2
        assert resultado[1].nome == "Maria Santos"
        assert resultado[1].email == "maria@example.com"
    
    @pytest.mark.asyncio
    async def test_obter_cliente_existente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = (1, "João Silva", "joao@example.com", "11999999999")
        
        resultado = await cliente_repositorio.obter_cliente(1)
        
        assert resultado is not None
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@example.com"
        assert resultado.telefone == "11999999999"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (1,)
        )
    
    @pytest.mark.asyncio
    async def test_obter_cliente_inexistente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.fetchone.return_value = None
        
        resultado = await cliente_repositorio.obter_cliente(999)
        
        assert resultado is None
    
    @pytest.mark.asyncio
    async def test_criar_cliente_sucesso(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.lastrowid = 1
        
        cliente_criar = ClienteCriarAtualizar(
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        
        resultado = await cliente_repositorio.criar_cliente(cliente_criar)
        
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@example.com"
        assert resultado.telefone == "11999999999"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?,?,?)",
            ("João Silva", "joao@example.com", "11999999999")
        )
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_existente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.rowcount = 1
        
        cliente_atualizar = ClienteCriarAtualizar(
            nome="João Silva Atualizado",
            email="joao.novo@example.com",
            telefone="11777777777"
        )
        
        resultado = await cliente_repositorio.atualizar_cliente(1, cliente_atualizar)
        
        assert resultado is not None
        assert resultado.id_ == 1
        assert resultado.nome == "João Silva Atualizado"
        assert resultado.email == "joao.novo@example.com"
        assert resultado.telefone == "11777777777"
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
            ("João Silva Atualizado", "joao.novo@example.com", "11777777777", 1)
        )
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_inexistente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.rowcount = 0
        
        cliente_atualizar = ClienteCriarAtualizar(
            nome="João Silva",
            email="joao@example.com",
            telefone="11999999999"
        )
        
        resultado = await cliente_repositorio.atualizar_cliente(999, cliente_atualizar)
        
        assert resultado is None
    
    @pytest.mark.asyncio
    async def test_deletar_cliente_existente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.rowcount = 1
        
        resultado = await cliente_repositorio.deletar_cliente(1)
        
        assert resultado is True
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "DELETE FROM clientes WHERE id = ?", (1,)
        )
    
    @pytest.mark.asyncio
    async def test_deletar_cliente_inexistente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.rowcount = 0
        
        resultado = await cliente_repositorio.deletar_cliente(999)
        
        assert resultado is False