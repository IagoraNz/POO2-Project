import sys
import os
import pytest

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from backend.back import Autenticacao
@pytest.fixture
def server() -> Autenticacao:
    """
    Summary:
        Essa função é um fixture que retorna uma instância de Autenticacao.
        
    Args:
        None
        
    Returns:
        Autenticacao: Uma instância de Autenticacao.
    """
    return Autenticacao(user="default_user", senha="default_senha")