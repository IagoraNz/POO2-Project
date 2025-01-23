from psycopg2 import sql
import psycopg2

class Aviao():
    """
    Classe que representa um avião.
    """
    def __init__(self, modelo: str, quantidade_assentos: int, sigla_av: str):
        """
        Inicializa um objeto Aviao.

        Args:
            modelo: (str) O modelo do avião.
            quantidade_assentos: (int) O número de assentos no avião.
            sigla_av: (str) A sigla única que identifica o avião.
        """
        self._modelo = modelo
        self._quantidade_assentos = quantidade_assentos
        self._sigla_av = sigla_av

    @property
    def modelo(self):        
        """Obtém o modelo do avião."""
        return self._modelo
    
    @modelo.setter
    def modelo(self, modelo: str):
        """Define o modelo do avião."""
        self._modelo = modelo

    @property
    def quantidade_assentos(self):
        """Obtém a quantidade de assentos do avião."""
        return self._quantidade_assentos
    
    @quantidade_assentos.setter
    def quantidade_assentos(self, quantidade_assentos: int):
        """Define a quantidade de assentos do avião."""
        self._quantidade_assentos = quantidade_assentos

    @property
    def sigla_av(self):
        """Obtém a sigla do avião."""
        return self._sigla_av

    @sigla_av.setter
    def sigla_av(self, sigla_av: str):
        """Define a sigla do avião."""
        self._sigla_av = sigla_av

class Voo():
    """
    Classe que representa um voo.
    """
    def __init__(self, sigla: str, origem: str, destino: str, aviao: object) -> None:
        """
        Inicializa um objeto Voo.

        Args:
            sigla: (str) A sigla única do voo.
            origem: (str) O local de origem do voo.
            destino: (str) O local de destino do voo.
            aviao: (Aviao) O avião associado ao voo.
        """
        self._sigla = sigla
        self._origem = origem
        self._destino = destino
        self._aviao = aviao
        self._assentos = []
        self._reservados = []
        
    @property
    def sigla(self):
        """Obtém a sigla do voo."""
        return self._sigla

    @sigla.setter
    def sigla(self, sigla: str):
        """Define a sigla do voo."""
        self._sigla = sigla

    @property
    def origem(self):
        """Obtém a origem do voo."""
        return self._origem

    @origem.setter
    def origem(self, origem: str):
        """Define a origem do voo."""
        self._origem = origem

    @property
    def destino(self):
        """Obtém o destino do voo."""
        return self._destino

    @destino.setter
    def destino(self, destino: str):
        """Define o destino do voo."""
        self._destino = destino

    @property
    def aviao(self):
        """Obtém o avião associado ao voo."""
        return self._aviao

    @aviao.setter
    def aviao(self, aviao: Aviao):
        """Define o avião associado ao voo."""
        self._aviao = aviao
        
    def preenche_assentos(self, quantidade: int) -> tuple[bool|str]:
        """
        Preenche os assentos do voo com base na quantidade especificada.

        Args:
            quantidade: (int) O número total de assentos disponíveis.

        Returns:
            tuple: (bool, str) Sucesso e mensagem informativa.
        """
        for i in range(1, quantidade + 1):
            self._assentos.append(i)
        return True, "Assentos preenchidos com sucesso."

    def reservar_assento(self, numero: int) -> tuple[bool|str]:
        """
        Reserva um assento específico no voo.

        Args:
            numero: (int) O número do assento a ser reservado.

        Returns:
            tuple: (bool, str) Sucesso e mensagem informativa.
        """
        if numero in self._assentos:
            self._assentos.remove(numero)
            self._reservados.append(numero)
            return True, "Assento reservado com sucesso."
        elif numero in self._reservados:
            return False, "Assento já está reservado."
        return False, "O número solicitado não existe."
    
class Passageiro:
    """
    Classe que representa um passageiro.

    """
    def __init__(self, nome: str, cpf: int, telefone: int) -> None:
        """
        Inicializa um objeto Passageiro.

        Args:
            nome: (str) O nome do passageiro.
            cpf: (int) O CPF do passageiro.
            telefone: (int) O telefone do passageiro.
        """
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone

    @property
    def nome(self):
        """Obtém o nome do passageiro."""
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        """Define o nome do passageiro."""
        self._nome = nome

    @property
    def cpf(self):
        """Obtém o CPF do passageiro."""
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: int):
        """Define o CPF do passageiro."""
        self._cpf = cpf

    @property
    def telefone(self):
        """Obtém o telefone do passageiro."""
        return self._telefone

    @telefone.setter
    def telefone(self, telefone: int):
        """Define o telefone do passageiro."""
        self._telefone = telefone 
        
class Funcionario():
    """
    Classe que representa um funcionário genérico.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str) -> None:
        """
        Inicializa um objeto Funcionario.

        Args:
            nome: (str) Nome do funcionário.
            cpf: (int) CPF do funcionário.
            salario: (float) Salário do funcionário.
            senha: (str) Senha para autenticação.
        """
        self._nome = nome
        self._cpf = cpf
        self._salario = salario
        self._senha = senha

    @property
    def nome(self):
        """Obtém o nome do funcionário."""
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        """Define o nome do funcionário."""
        self._nome = nome

    @property
    def cpf(self):
        """Obtém o CPF do funcionário."""
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf: int):
        """Define o CPF do funcionário."""
        self._cpf = cpf

    @property
    def salario(self):
        """Obtém o salário do funcionário."""
        return self._salario
    
    @salario.setter
    def salario(self, salario: float):
        """Define o salário do funcionário."""
        self._salario = salario

    @property
    def senha(self):
        """Obtém a senha do funcionário."""
        return self._senha
    
    @senha.setter
    def senha(self, senha: str):
        """Define a senha do funcionário."""
        self._senha = senha 
        
class Gerente(Funcionario):
    """
    Classe que representa um gerente, herda de Funcionario.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, expediente: str):
        """
        Inicializa um objeto Gerente.

        Args:
            nome: (str) Nome do gerente.
            cpf: (int) CPF do gerente.
            salario: (float) Salário do gerente.
            senha: (str) Senha do gerente para autenticação.
            expediente: (str) Horário de expediente do gerente.
        """
        super().__init__(nome, cpf, salario, senha)
        self._expediente = expediente

    @property
    def expediente(self):
        """Obtém o horário de expediente do gerente."""
        return self._expediente
    
    @expediente.setter
    def expediente(self, expediente: str):
        """Define o horário de expediente do gerente."""
        self._expediente = expediente

class Atendente(Funcionario):
    """
    Classe que representa um atendente, herda de Funcionario.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, terminal: int):
        """
        Inicializa um objeto Atendente.

        Args:
            nome: (str) Nome do atendente.
            cpf: (int) CPF do atendente.
            salario: (float) Salário do atendente.
            senha: (str) Senha do atendente para autenticação.
            terminal: (int) Número do terminal de trabalho.
        """
        super().__init__(nome, cpf, salario, senha)
        self._terminal = terminal

    @property
    def terminal(self):
        """Obtém o número do terminal do atendente."""
        return self._terminal
    
    @terminal.setter
    def terminal(self, terminal: int):
        """Define o número do terminal do atendente."""
        self._terminal = terminal

class Autenticacao:
    """
    Classe responsável por gerenciar a autenticação de usuários.
    """
    def __init__(self, user: str, senha: str): 
        """
        Inicializa a classe de autenticação e conecta ao banco de dados.

        Args:
            user (str): Nome de usuário.
            senha (str): Senha do usuário.

        Raises:
            ConnectionError: Caso não seja possível conectar ao banco de dados.
        """
        self._user = user
        self._senha = senha
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',  # Nome do banco de dados especificado no Docker
                user='poodois',        # Nome do usuário especificado no Docker
                password='1234',       # Senha especificada no Docker
                host='localhost',
                port=5432
            )
            self.criar_tabela()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        """
        Cria a tabela de credenciais no banco de dados, caso não exista.
        """
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS credenciais (
                    user_name TEXT PRIMARY KEY,
                    senha TEXT NOT NULL,
                    tipo INT NOT NULL
                );
            ''')
            self.conn.commit()

    @property
    def user(self):
        """Obtém o nome de usuário."""
        return self._user

    @user.setter
    def user(self, user: str):
        """Define o nome de usuário."""
        self._user = user

    @property
    def senha(self):
        """Obtém a senha do usuário."""
        return self._senha

    @senha.setter
    def senha(self, senha: str):
        """Define a senha do usuário."""
        self._senha = senha

    def cadastro(self, user: str, senha: str, tipo: int) -> tuple[bool|str]:
        """
        Cadastra um novo usuário no banco de dados.

        Args:
            user: (str) Nome de usuário.
            senha: (str) Senha do usuário.
            tipo: (int) Tipo de usuário (1 - Gerente, 2 - Atendente).

        Returns:
            tuple: (bool|str) Sucesso do cadastro e mensagem correspondente.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO credenciais (user_name, senha, tipo)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_name) DO UPDATE
                        SET senha = EXCLUDED.senha, tipo = EXCLUDED.tipo;
                    """),
                    (user, senha, tipo)
                )
                self.conn.commit()
            return True, "Cadastro efetuado com sucesso"
        except Exception as e:
            return False, f"Erro no cadastro: {str(e)}"

    def login(self, user: str, senha: str) -> tuple[bool|str]:
        """
        Realiza a autenticação de um usuário.

        Args:
            user: (str) Nome de usuário.
            senha: (str) Senha do usuário.

        Returns:
            tuple: (bool|str) Resultado do login e mensagem correspondente.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL("""
                        SELECT senha, tipo FROM credenciais WHERE user_name = %s;
                    """),
                    (user,)
                )
                resultado = cur.fetchone()

                if resultado:
                    senha_armazenada, tipo = resultado
                    if senha_armazenada == senha:
                        if tipo == 1:
                            return 1, "Login efetuado com sucesso, Gerente"
                        elif tipo == 2:
                            return 2, "Login efetuado com sucesso, Atendente"
                return False, "Login não foi efetuado com sucesso"
        except Exception as e:
            return False, f"Erro no login: {str(e)}"
    
class CiaAerea():
    """ Classe para representar uma companhia aérea."""
    def __init__(self, nome: str, cnpj: int, telefone: int, endereco: str) -> None:
        """
        Inicializa uma nova instância da classe CiaAerea.

        Args:
            nome: (str) Nome da companhia aérea.
            cnpj: (int) CNPJ da companhia aérea.
            telefone: (int) Telefone de contato da companhia aérea.
            endereco: (str) Endereço da companhia aérea.
        """
        self._nome = nome
        self._cnpj = cnpj
        self._telefone = telefone
        self._endereco = endereco
        self._avioes = {}
        self._voos = {}
        self._passageiros = {}
        self._funcionarios = {}

    @property
    def nome(self) -> str:
        """Retorna o nome da companhia aérea."""
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        """Define o nome da companhia aérea."""
        self._nome = nome

    @property
    def cnpj(self) -> int:
        """Retorna o CNPJ da companhia aérea."""
        return self._cnpj
    
    @cnpj.setter
    def cnpj(self, cnpj: int):
        """Define o CNPJ da companhia aérea."""
        self._cnpj = cnpj

    @property
    def telefone(self) -> int:
        """Retorna o telefone de contato da companhia aérea."""
        return self._telefone
    
    @telefone.setter
    def telefone(self, telefone: int):
        """Define o telefone de contato da companhia aérea."""
        self._telefone = telefone

    @property
    def endereco(self) -> str:
        """Retorna o endereço da companhia aérea."""
        return self._endereco
    
    @endereco.setter
    def endereco(self, endereco: str):
        """Define o endereço da companhia aérea."""
        self._endereco = endereco

    def add_aviao(self, aviao: object) -> tuple[bool|str]:
        """
        Adiciona um avião ao dicionário de aviões.

        Args:
            aviao: (object) Instância de Aviao a ser adicionada.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if isinstance(aviao, Aviao):
            if aviao.sigla_av not in self._avioes:
                self._avioes[aviao.sigla_av] = aviao
                return True, "Avião cadastrado com sucesso!"
            return False, "Avião já cadastrado!"
        return False, "Avião inválido!"

    def excluir_aviao(self, sigla: str) -> tuple[bool|str]:
        """
        Exclui um avião do dicionário de aviões.

        Args:
            sigla: (str) Sigla do avião a ser excluído.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if sigla in self._avioes:
            del self._avioes[sigla]
            return True, "Avião excluído com sucesso!"
        return False, "Avião não encontrado!"

    def add_voo(self, voo: object) -> tuple[bool|str]:
        """
        Adiciona um voo ao dicionário de voos.

        Args:
            voo: (object) Instância de Voo a ser adicionada.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if isinstance(voo, Voo):
            if voo.sigla not in self._voos:
                self._voos[voo.sigla] = voo
                return True, "Voo cadastrado com sucesso!"
            return False, "Voo já cadastrado!"
        return False, "Voo inválido!"

    def excluir_voo(self, sigla: str) -> tuple[bool|str]:
        """
        Exclui um voo do dicionário de voos.

        Args:
            sigla: (str) Sigla do voo a ser excluído.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if sigla in self._voos:
            del self._voos[sigla]
            return True, "Voo excluído com sucesso!"
        return False, "Voo não encontrado!"

    def add_passageiro(self, passageiro: object) -> tuple[bool|str]:
        """
        Adiciona um passageiro ao dicionário de passageiros.

        Args:
            passageiro: (object) Instância de Passageiro a ser adicionada.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if isinstance(passageiro, Passageiro):
            if passageiro.cpf not in self._passageiros:
                self._passageiros[passageiro.cpf] = passageiro
                return True, "Passageiro cadastrado com sucesso!"
            return False, "Passageiro já cadastrado!"
        return False, "Passageiro inválido!"

    def excluir_passageiro(self, cpf: int) -> tuple[bool|str]:
        """
        Exclui um passageiro do dicionário de passageiros.

        Args:
            cpf: (int) CPF do passageiro a ser excluído.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if cpf in self._passageiros:
            del self._passageiros[cpf]
            return True, "Passageiro excluído com sucesso!"
        return False, "Passageiro não encontrado!"

    def add_funcionario(self, funcionario: object) -> tuple[bool|str]:
        """
        Adiciona um funcionário ao dicionário de funcionários.

        Args:
            funcionario: (object) Instância de Funcionario a ser adicionada.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if isinstance(funcionario, Funcionario):
            if funcionario.cpf not in self._funcionarios:
                self._funcionarios[funcionario.cpf] = funcionario
                return True, "Funcionário cadastrado com sucesso!"
            return False, "Funcionário já cadastrado!"
        return False, "Funcionário inválido!"

    def excluir_funcionario(self, cpf: int) -> tuple[bool|str]:
        """
        Exclui um funcionário do dicionário de funcionários.

        Args:
            cpf: (int) CPF do funcionário a ser excluído.

        Returns:
            tuple: (bool, str) Indica o sucesso ou falha e uma mensagem.
        """
        if cpf in self._funcionarios:
            del self._funcionarios[cpf]
            return True, "Funcionário excluído com sucesso!"
        return False, "Funcionário não encontrado!"