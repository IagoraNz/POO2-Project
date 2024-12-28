import redis

class Aviao():
    def __init__(self, modelo: str, quantidade_assentos: int, sigla_av: str):
        self._modelo = modelo
        self._quantidade_assentos = quantidade_assentos
        self._sigla_av = sigla_av

    @property
    def modelo(self):
        return self._modelo
    
    @modelo.setter
    def modelo(self, modelo: str):
        self._modelo = modelo

    @property
    def quantidade_assentos(self):
        return self._quantidade_assentos
    
    @quantidade_assentos.setter
    def quantidade_assentos(self, quantidade_assentos: int):
        self._quantidade_assentos = quantidade_assentos

    @property
    def sigla_av(self):
        return self._sigla_av

    @sigla_av.setter
    def sigla_av(self, sigla_av: str):
        self._sigla_av = sigla_av

class Voo():
    def __init__(self, sigla: str, origem: str, destino: str, aviao: object) -> None:
        self._sigla = sigla
        self._origem = origem
        self._destino = destino
        self._aviao = aviao
        self._assentos = []
        self._reservados = []
        
    @property
    def sigla(self):
        return self._sigla
    
    @sigla.setter
    def sigla(self, sigla: str):
        self._sigla = sigla
    
    @property 
    def origem(self):
        return self._origem
    
    @origem.setter
    def origem(self, origem: str):
        self._origem = origem
    
    @property
    def destino(self):
        return self._destino
    
    @destino.setter
    def destino(self, destino: str):
        self._destino = destino
    
    @property
    def aviao(self):
        return self._aviao
    
    @aviao.setter
    def aviao(self, aviao: object):
        self._aviao = aviao
        
    def preenche_assentos(self, quantidade) -> tuple:
        for i in range(i, quantidade - 1):
            self._assentos.append(i)
        return True, 'Assentos preenchidos com sucesso'
    
    def reservar_assento(self, numero) -> tuple:
        if numero in self._assentos:
            self._assentos.remove(numero)
            self._reservados.append(numero)
            return True, 'Assento reservado com sucesso'
        elif numero in self._reservados:
            return False, 'Assento já está reservado'
        return False, 'O número solicitado não existe'
    
class Passageiro:
    def __init__(self, nome: str, cpf: int, telefone: int) -> None:
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def set_nome(self, nome: str):
        self._nome = nome

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def set_cpf(self, cpf: int):
        self._cpf = cpf

    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def set_telefone(self, telefone: int):
        self._telefone = telefone  
        
class Funcionario():
    def __init__(self, nome: str, cpf: int, salario: float, senha: str) -> None:
        self._nome = nome
        self._cpf = cpf
        self._salario = salario
        self._senha = senha

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def salario(self):
        return self._salario
    
    @salario.setter
    def salario(self, salario):
        self._salario = salario

    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, senha):
        self._senha = senha 
        
class Gerente(Funcionario):
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, expediente: str):
        super().__init__(nome, cpf, salario, senha)
        self._expediente = expediente

    @property
    def expediente(self):
        return self._expediente
    
    @expediente.setter
    def expediente(self, expediente: str):
        self._expediente = expediente
        
class Atendente(Funcionario):
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, terminal: int):
        super().__init__(nome, cpf, salario, senha)
        self._terminal = terminal

    @property
    def terminal(self):
        return self._terminal
    
    @terminal.setter
    def terminal(self, terminal: int):
        self._terminal = terminal

class Autenticacao:
    def __init__(self, user: str, senha: str):
        self._user = user
        self._senha = senha
        
    @property
    def user(self):
        return self._user
        
    @user.setter
    def user(self, user: str):
        self._user = user
        
    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, senha: str):
        self._senha = senha
        
    def cadastro(self, user: str, senha: str, tipo: int) -> tuple:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if not r.exists('credenciais'):
            r.hset('credenciais', mapping={user: f"{senha},{tipo}"})
        else:
            r.hset('credenciais', user, f"{senha},{tipo}")
        return True, "Cadastro efetuado com sucesso"
            
    def login(self, user: str, senha: str) -> tuple:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if r.exists('credenciais'):
            dados = r.hget('credenciais', user)
            if dados:
                senha_armazenada, tipo = dados.decode('utf-8').split(',')
                if senha_armazenada == senha:
                    if int(tipo) == 1:
                        return 1, "Login efetuado com sucesso"
                    elif int(tipo) == 2:
                        return 2, "Login efetuado com sucesso"
        return False, "Login não foi efetuado com sucesso"
    
class CiaAerea():
    def __init__(self, nome: str, cnpj: int, telefone: int, endereco: str):
        self._nome = nome
        self._cnpj = cnpj
        self._telefone = telefone
        self._endereco = endereco
        self._avioes = {}
        self._voos = {}
        self._passageiros = {}
        self._funcionarios = {}

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def cnpj(self):
        return self._cnpj
    
    @cnpj.setter
    def cnpj(self, cnpj: int):
        self._cnpj = cnpj

    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone(self, telefone: int):
        self._telefone = telefone

    @property
    def endereco(self):
        return self._endereco
    
    @endereco.setter
    def endereco(self, endereco: str):
        self._endereco = endereco
        
    def add_aviao(self, aviao: object) -> tuple:
        if isinstance(aviao, Aviao):
            if aviao._sigla_av not in self._avioes.keys():
                self._avioes[aviao.sigla_av] = aviao
                return True, 'Avião cadastrado com sucesso!'
            return False, 'Avião já cadastrado!'
        return False, 'Avião inválido!'
    
    def excluir_aviao(self, sigla: str) -> tuple:
        if sigla in self._avioes.keys():
            del self._avioes[sigla]
            return True, 'Avião excluído com sucesso!'
        return False, 'Avião não encontrado!'

    def add_voo(self, voo: object) -> tuple:
        if isinstance(voo, Voo):
            if voo.sigla not in self._voos:
                self._voos[voo.sigla] = voo
                return True, 'Voo cadastrado com sucesso!'
            return False, 'Voo já cadastrado!'
        return False, 'Voo inválido!'
    
    def excluir_voo(self, sigla: str) -> tuple:
        if sigla in self._voos.keys():
            del self._voos[sigla]
            return True, 'Voo excluído com sucesso!'
        return False, 'Voo não encontrado!'
    
    def add_passageiro(self, passageiro: object) -> tuple:
        if isinstance(passageiro, Passageiro):
            if passageiro.cpf not in self._passageiros:
                self._passageiros[passageiro.cpf] = passageiro
                return True, 'Passageiro cadastrado com sucesso!'
            return False, 'Passageiro já cadastrado!'
        return False, 'Passageiro inválido!'
    
    def excluir_passageiro(self, cpf: int) -> tuple:
        if cpf in self._passageiros.keys():
            del self._passageiros[cpf]
            return True, 'Passageiro excluído com sucesso!'
        return False, 'Passageiro não encontrado!'
    
    def add_funcionario(self, funcionario: object) -> tuple:
        if isinstance(funcionario, Funcionario):
            if funcionario.cpf not in self._funcionarios:
                self._funcionarios[funcionario.cpf] = funcionario
                return True, "Funcionário cadastrado com sucesso!"
            return False, "Funcionário já cadastrado!"
        return False, "Funcionário inválido!"
    
    def excluir_funcionario(self, cpf: object) -> tuple:
        if cpf in self._funcionarios.keys():
            del self._funcionarios[cpf]
            return True, "Funcionário excluído com sucesso!"
        return False, "Funcionário não encontrado!"