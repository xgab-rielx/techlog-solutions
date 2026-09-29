# Techlog Solutions

Sistema web para gerenciamento de chamados, desenvolvido com Python e FastAPI.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Jinja2
- SQLite
- HTML, CSS e JavaScript
- Pytest

## Funcionalidades

- Cadastro de usuários
- Login de usuários
- Cadastro de clientes
- Abertura e gerenciamento de chamados
- Testes automatizados

## Pré-requisitos

- Python 3.10 ou superior
- Git

## Instalação

Clone o repositório:

```bash
git clone [https://github.com/xgab-rielx/techlog-solutions.git](https://github.com/SEU-USUARIO/techlog-solutions.git)
cd techlog-solutions
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Com o ambiente virtual ativado, execute:

```bash
uvicorn app.main:app --reload
```

Depois, abra no navegador:

```text
http://127.0.0.1:8000
```

## Testes

Para executar os testes automatizados:

```bash
pytest
```

## Segurança

Os arquivos abaixo não devem ser enviados ao GitHub:

- `.env`
- `venv/`
- `techlog.db`
- `__pycache__/`

Esses arquivos estão configurados no `.gitignore`.

## Autor

Gabriel Vicente — projeto desenvolvido para estudo de Python, FastAPI e desenvolvimento web.