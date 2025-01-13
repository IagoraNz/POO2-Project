import pytest
import redis

def test_login_gerente(server):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    r.hset('credenciais', mapping={'gerente': 'senha123,1'})  
    
    status, mensagem = server.login('gerente', 'senha123')
    assert status == 1
    assert mensagem == "Login efetuado com sucesso, Gerente"

def test_login_atendente(server):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    r.hset('credenciais', mapping={'atendente': 'senha456,2'})  
    
    status, mensagem = server.login('atendente', 'senha456')
    assert status == 2
    assert mensagem == "Login efetuado com sucesso, Atendente"

def test_login_falha(server):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()  
    
    status, mensagem = server.login('usuario_inexistente', 'senha_errada')
    assert status == False
    assert mensagem == "Login não foi efetuado com sucesso"