import pytest
import redis

def test_login_gerente(server) -> None:
    """
    Summary:
        Testa o login de um gerente.
        
        Neste teste, a função verifica se o login do usuário 'gerente' é realizado corretamente com a senha
        'senha123'. A função valida se o status retornado é 1 e se a mensagem retornada é "Login efetuado com 
        sucesso, Gerente".

    Args:
        server: Instância do servidor onde o login será testado.
        
    Returns:
        None

    Assert:
        status: (int) 1, indicando sucesso no login do gerente.
        mensagem: (str) Mensagem indicando o sucesso do login para o gerente.
    """
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    r.hset('credenciais', mapping={'gerente': 'senha123,1'})  
    
    status, mensagem = server.login('gerente', 'senha123')
    assert status == 1
    assert mensagem == "Login efetuado com sucesso, Gerente"

def test_login_atendente(server) -> None:
    """
    Summary:
        Testa o login de um atendente.
        
        Neste teste, a função verifica se o login do usuário 'atendente' é realizado corretamente com a senha
        'senha456'. A função valida se o status retornado é 2 e se a mensagem retornada é "Login efetuado com 
        sucesso, Atendente".

    Args:
        server: Instância do servidor onde o login será testado.

    Assert:
        status: (int) 2, indicando sucesso no login do atendente.
        mensagem: (str) Mensagem indicando o sucesso do login para o atendente.
    """
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    r.hset('credenciais', mapping={'atendente': 'senha456,2'})  
    
    status, mensagem = server.login('atendente', 'senha456')
    assert status == 2
    assert mensagem == "Login efetuado com sucesso, Atendente"

def test_login_falha(server) -> None:
    """
    Summary:
        Testa o login com falha (usuário inexistente ou senha incorreta).
        
        Este teste verifica se o login falha quando um usuário não existente ou senha incorreta é fornecido.
        A função valida se o status retornado é False e se a mensagem é "Login não foi efetuado com sucesso".

    Args:
        server: Instância do servidor onde o login será testado.
        
    Returns:
        None

    Assert:
        status: (bool) False, indicando falha no login.
        mensagem: (str) Mensagem indicando falha no login.
    """
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    
    status, mensagem = server.login('usuario_inexistente', 'senha_errada')
    assert status == False
    assert mensagem == "Login não foi efetuado com sucesso"