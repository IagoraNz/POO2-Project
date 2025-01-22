from psycopg2 import sql
import psycopg2

class Aviao():
    """
    Classe que representa um avião.

    Atributos:
        modelo (str): Modelo do avião.
        quantidade_assentos (int): Quantidade de assentos disponíveis no avião.
        sigla_av (str): Sigla identificadora do avião.
    """
    def __init__(self, modelo: str, quantidade_assentos: int, sigla_av: str):
        """
        Inicializa a classe Aviao.

        Args:
            modelo (str): Modelo do avião.
            quantidade_assentos (int): Quantidade de assentos disponíveis.
            sigla_av (str): Sigla identificadora do avião.
        """
        self._modelo = modelo
        self._quantidade_assentos = quantidade_assentos
        self._sigla_av = sigla_av

    @property
    def modelo(self) -> str:
        """Retorna o modelo do avião"""
        return self._modelo
    
    @modelo.setter
    def modelo(self, modelo: str):
        """Define o modelo do avião"""
        self._modelo = modelo

    @property
    def quantidade_assentos(self) -> int:
        """Retorna a quantidade de assentos do avião"""
        return self._quantidade_assentos
    
    @quantidade_assentos.setter
    def quantidade_assentos(self, quantidade_assentos: int):
        """Define a quantidade de assentos do avião"""
        self._quantidade_assentos = quantidade_assentos

    @property
    def sigla_av(self) -> str:
        """Retorna a sigla identificadora do avião"""
        return self._sigla_av

    @sigla_av.setter
    def sigla_av(self, sigla_av: str):
        """Define a sigla identificadora do avião."""
        self._sigla_av = sigla_av

class Voo():
    """
    Classe que representa um voo.

    Atributos:
        sigla (str): Identificador único do voo.
        origem (str): Cidade de origem do voo.
        destino (str): Cidade de destino do voo.
        aviao (Aviao): Avião associado ao voo.
    """
    def __init__(self, sigla: str, origem: str, destino: str, aviao: object) -> None:
        """
        Inicializa a classe Voo.

        Args:
            sigla (str): Identificador do voo.
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            aviao (Aviao): Avião utilizado no voo.
        """
        self._sigla = sigla
        self._origem = origem
        self._destino = destino
        self._aviao = aviao
        self._assentos = []
        self._reservados = []
        
    @property
    def sigla(self) -> str:
        """Retorna a sigla do voo."""
        return self._sigla
    
    @sigla.setter
    def sigla(self, sigla: str):
        """Define a sigla do voo."""
        self._sigla = sigla
    
    @property 
    def origem(self) -> str:
        """Retorna a cidade de origem do voo."""
        return self._origem
    
    @origem.setter
    def origem(self, origem: str):
        """Define a cidade de origem do voo."""
        self._origem = origem
    
    @property
    def destino(self) ->  str:
        """Retorna a cidade de destino do voo."""
        return self._destino
    
    @destino.setter
    def destino(self, destino: str):
        """Define a cidade de destino do voo."""
        self._destino = destino
    
    @property
    def aviao(self) -> Aviao:
        """Retorna o avião associado ao voo."""
        return self._aviao
    
    @aviao.setter
    def aviao(self, aviao: Aviao):
        """Define o avião associado ao voo."""
        self._aviao = aviao
        
    def preenche_assentos(self, quantidade: int) -> tuple:
        """
        Preenche a lista de assentos disponíveis no voo.

        Args:
            quantidade (int): Quantidade de assentos a preencher.

        Returns:
            tuple: (bool, str) indicando o sucesso e uma mensagem.
        """
        for i in range(i, quantidade - 1):
            self._assentos.append(i)
        return True, 'Assentos preenchidos com sucesso'
    
    def reservar_assento(self, numero: int) -> tuple:
        """
        Reserva um assento no voo.

        Args:
            numero (int): Número do assento a ser reservado.

        Returns:
            tuple: (bool, str) indicando o sucesso e uma mensagem.
        """
        if numero in self._assentos:
            self._assentos.remove(numero)
            self._reservados.append(numero)
            return True, 'Assento reservado com sucesso'
        elif numero in self._reservados:
            return False, 'Assento já está reservado'
        return False, 'O número solicitado não existe'
    
class Passageiro:
    """
    Classe que representa um passageiro.

    Atributos:
        nome (str): Nome do passageiro.
        cpf (int): CPF do passageiro.
        telefone (int): Número de telefone do passageiro.
    """
    def __init__(self, nome: str, cpf: int, telefone: int) -> None:
        """
        Inicializa a classe Passageiro.

        Args:
            nome (str): Nome do passageiro.
            cpf (int): CPF do passageiro.
            telefone (int): Número de telefone do passageiro.
        """
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone

    @property
    def nome(self) -> str:
        """Retorna o nome do passageiro."""
        return self._nome
    
    @nome.setter
    def set_nome(self, nome: str):
        """Define o nome do passageiro"""
        self._nome = nome

    @property
    def cpf(self) -> int:
        """Obtém o CPF do passageiro"""
        return self._cpf
    
    @cpf.setter
    def set_cpf(self, cpf: int):
        """Define o CPF do passageiro"""
        self._cpf = cpf

    @property
    def telefone(self) -> int:
        """Obtém o telefone do passageiro."""
        return self._telefone
    
    @telefone.setter
    def set_telefone(self, telefone: int):
        """Define o telefone do passageiro."""
        self._telefone = telefone  
        
class Funcionario():
    """
    Representa um funcionário com nome, CPF, salário e senha.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str) -> None:
        """
        Inicializa um objeto Funcionario.

        Args:
            nome (str): Nome do funcionário.
            cpf (int): CPF do funcionário.
            salario (float): Salário do funcionário.
            senha (str): Senha do funcionário.
        """
        self._nome = nome
        self._cpf = cpf
        self._salario = salario
        self._senha = senha

    @property
    def nome(self) -> str:
        """Obtém o nome do funcionário."""
        return self._nome
    
    @nome.setter
    def nome(self, nome : str):
        """Define o nome do funcionário."""
        self._nome = nome

    @property
    def cpf(self) -> int:
        """Obtém o CPF do funcionário."""
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf: int):
        """Define o CPF do funcionário."""
        self._cpf = cpf

    @property
    def salario(self) -> float:
        """Obtém o salário do funcionário."""
        return self._salario
    
    @salario.setter
    def salario(self, salario: float):
        """Define o salário do funcionário."""
        self._salario = salario

    @property
    def senha(self) -> str:
        """Obtém a senha do funcionário."""
        return self._senha
    
    @senha.setter
    def senha(self, senha: str):
        """Define a senha do funcionário."""
        self._senha = senha 
        
class Gerente(Funcionario):
    """
    Representa um gerente que herda de Funcionario, com atributo adicional expediente.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, expediente: str):
        """
        Inicializa um objeto Gerente.

        Args:
            nome (str): Nome do gerente.
            cpf (int): CPF do gerente.
            salario (float): Salário do gerente.
            senha (str): Senha do gerente.
            expediente (str): Horário de expediente do gerente.
        """
        super().__init__(nome, cpf, salario, senha)
        self._expediente = expediente

    @property
    def expediente(self) -> str:
        """Obtém o horário de expediente do gerente."""
        return self._expediente
    
    @expediente.setter
    def expediente(self, expediente: str):
        """Define o horário de expediente do gerente."""
        self._expediente = expediente
        
class Atendente(Funcionario):
    """
    Representa um atendente que herda de Funcionario, com atributo adicional terminal.
    """
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, terminal: int):
        """
        Inicializa um objeto Atendente.

        Args:
            nome (str): Nome do atendente.
            cpf (int): CPF do atendente.
            salario (float): Salário do atendente.
            senha (str): Senha do atendente.
            terminal (int): Terminal atribuído ao atendente.
        """
        super().__init__(nome, cpf, salario, senha)
        self._terminal = terminal

    @property
    def terminal(self) -> int:
        """Obtém o terminal atribuído ao atendente."""
        return self._terminal
    
    @terminal.setter
    def terminal(self, terminal: int):
        """Define o terminal atribuído ao atendente."""
        self._terminal = terminal

class Autenticacao:
    """
    Responsável pela autenticação de usuários e gerenciamento de credenciais no banco de dados.
    """
    def __init__(self, user: str, senha: str):
        """
        Inicializa um objeto Autenticacao.

        Args:
            user (str): Nome de usuário.
            senha (str): Senha do usuário.
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
        Cria a tabela de credenciais no banco de dados, se ela não existir.
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
    def user(self) -> str:
        """Obtém o nome de usuário."""
        return self._user

    @user.setter
    def user(self, user: str):
        """Define o nome de usuário."""
        self._user = user

    @property
    def senha(self) -> str:
        """Obtém a senha do usuário."""
        return self._senha

    @senha.setter
    def senha(self, senha: str):
        """Define a senha do usuário."""
        self._senha = senha

    def cadastro(self, user: str, senha: str, tipo: int) -> tuple:
        """
        Cadastra ou atualiza um usuário no banco de dados.

        Args:
            user (str): Nome de usuário.
            senha (str): Senha do usuário.
            tipo (int): Tipo de usuário (1 para gerente, 2 para atendente).

        Returns:
            tuple: Status e mensagem de sucesso ou erro.
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

    def login(self, user: str, senha: str) -> tuple:
        """
        Realiza o login de um usuário.

        Args:
            user (str): Nome de usuário.
            senha (str): Senha do usuário.

        Returns:
            tuple: Status e mensagem indicando o tipo de usuário ou erro.
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
    """
    Representa uma companhia aérea, com atributos para gerenciar aviões, voos, passageiros e funcionários.
    """
    def __init__(self, nome: str, cnpj: int, telefone: int, endereco: str):
        """
        Inicializa um objeto CiaAerea.

        Args:
            nome (str): Nome da companhia aérea.
            cnpj (int): CNPJ da companhia aérea.
            telefone (int): Telefone da companhia aérea.
            endereco (str): Endereço da companhia aérea.
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
        """Obtém o nome da companhia aérea."""
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        """Define o nome da companhia aérea."""
        self._nome = nome

    @property
    def cnpj(self) -> int:
        """Obtém o CNPJ da companhia aérea."""
        return self._cnpj
    
    @cnpj.setter
    def cnpj(self, cnpj: int):
        """Define o CNPJ da companhia aérea."""
        self._cnpj = cnpj

    @property
    def telefone(self) -> int:
        """Obtém o telefone da companhia aérea."""
        return self._telefone
    
    @telefone.setter
    def telefone(self, telefone: int):
        """Define o telefone da companhia aérea."""
        self._telefone = telefone

    @property
    def endereco(self) -> str:
        """Obtém o endereço da companhia aérea."""
        return self._endereco
    
    @endereco.setter
    def endereco(self, endereco: str):
        """Define o endereço da companhia aérea."""
        self._endereco = endereco
        
    def add_aviao(self, aviao: object) -> tuple:
        """
        Adiciona um avião à companhia aérea.

        Args:
            aviao (object): Objeto da classe Aviao.

        Returns:
            tuple: Status e mensagem indicando sucesso ou erro.
        """
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
    

class CadastroClientes:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',  # Nome do banco de dados
                user='poodois',        # Nome do usuário
                password='1234',       # Senha do usuário
                host='localhost',
                port=5432
            )

            self.criar_tabela()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        """Cria a tabela de clientes caso não exista."""
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT NOT NULL
                );
            ''')
            self.conn.commit()

    def cadastrar_cliente(self, nome: str, cpf: str, telefone: str) -> tuple:
        """Insere ou atualiza os dados de um cliente no banco de dados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL('''
                        INSERT INTO clientes (nome, cpf, telefone)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (cpf) DO UPDATE
                        SET nome = EXCLUDED.nome, telefone = EXCLUDED.telefone;
                    '''),
                    (nome, cpf, telefone)
                )
                self.conn.commit()
            return True, "Cliente cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar cliente: {str(e)}"

    # def listar_clientes(self):
    #     """Retorna uma lista com todos os clientes cadastrados."""
    #     try:
    #         with self.conn.cursor() as cur:
    #             cur.execute("SELECT id, nome, cpf, telefone FROM clientes;")
    #             clientes = cur.fetchall()
    #         return clientes
    #     except Exception as e:
    #         return []

    def buscar_cliente_por_cpf(self, cpf: str) -> tuple:
        """Busca um cliente pelo CPF."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, nome, cpf, telefone FROM clientes WHERE cpf = %s;",
                    (cpf,)
                )
                cliente = cur.fetchone()
            if cliente:
                return cliente
            return None
        except Exception as e:
            return None

    def excluir_cliente(self, cpf: str) -> tuple:
        """Exclui um cliente pelo CPF."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM clientes WHERE cpf = %s;",
                    (cpf,)
                )
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Cliente excluído com sucesso."
                return False, "Cliente não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir cliente: {str(e)}"
    
    def alterar_cliente(self, cpf: str, novo_nome: str, novo_telefone: str) -> tuple:
        """Altera os dados de um cliente existente pelo CPF."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE clientes 
                    SET nome = %s, telefone = %s 
                    WHERE cpf = %s;
                    ''',
                    (novo_nome, novo_telefone, cpf)
                )
                self.conn.commit()

                if cur.rowcount > 0:
                    return True, "Dados do cliente alterados com sucesso."
                else:
                    return False, "Cliente não encontrado."
        except Exception as e:
            return False, f"Erro ao alterar cliente: {str(e)}"


class CadastroVoos:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',         # Nome do banco de dados
                user='poodois',        # Nome do usuário
                password='1234',       # Senha do usuário
                host='localhost',
                port=5432
            )
            self.criar_tabela()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        """Cria a tabela de voos caso não exista."""
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS voos (
                    id SERIAL PRIMARY KEY,
                    sigla TEXT NOT NULL,
                    origem TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    modelo_aviao TEXT NOT NULL,
                    quantidade_assentos INTEGER NOT NULL
                );
            ''')
            self.conn.commit()

    def cadastrar_voo(self, sigla: str, origem: str, destino: str, modelo_aviao: str, quantidade_assentos: int) -> tuple:
        """Insere os dados de um voo no banco de dados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL('''
                        INSERT INTO voos (sigla, origem, destino, modelo_aviao, quantidade_assentos)
                        VALUES (%s, %s, %s, %s, %s)
                    '''), 
                    (sigla, origem, destino, modelo_aviao, quantidade_assentos)
                )
                self.conn.commit()
            return True, "Voo cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar voo: {str(e)}"

    def listar_voos(self) -> list:
        """Retorna uma lista com todos os voos cadastrados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
                voos = cur.fetchall()
            return voos
        except Exception as e:
            return []

    def buscar_voo_por_sigla(self, sigla: str) -> tuple:
        """Busca um voo pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, sigla, origem, destino, modelo_aviao FROM voos WHERE sigla = %s;",
                    (sigla,)
                )
                voo = cur.fetchone()
            if voo:
                return voo
            return None
        except Exception as e:
            return None

    def excluir_voo(self, sigla: str) -> tuple:
        """Exclui um voo pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM voos WHERE sigla = %s;",
                    (sigla,)
                )
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Voo excluído com sucesso."
                return False, "Voo não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir voo: {str(e)}"

    def alterar_voo(self, sigla: str, origem: str, destino: str, modelo_aviao: str, quantidade_assentos: int) -> tuple:
        """Altera os dados de um voo existente pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE voos 
                    SET origem = %s, destino = %s, modelo_aviao = %s, quantidade_assentos = %s
                    WHERE sigla = %s;
                    ''',
                    (origem, destino, modelo_aviao, quantidade_assentos, sigla)
                )
                self.conn.commit()

                if cur.rowcount > 0:
                    return True, "Dados do voo alterados com sucesso."
                else:
                    return False, "Voo não encontrado."
        except Exception as e:
            return False, f"Erro ao alterar voo: {str(e)}"

class BackendReservas:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',
                user='poodois',
                password='1234',
                host='localhost',
                port=5432
            )
            self.cur = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_table(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS voos (
                    id SERIAL PRIMARY KEY,
                    sigla TEXT NOT NULL,
                    origem TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    modelo_aviao TEXT NOT NULL,
                    quantidade_assentos INTEGER NOT NULL
                );
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

    def listar_voos(self):
        try:
            self.cur.execute("SELECT sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
            voos = self.cur.fetchall()
            return voos
        except Exception as e:
            print(f"Erro ao listar voos: {e}")
            return []

    def reservar_voo(self, sigla, assento):
        try:
            # Verificar se o voo existe e há assentos disponíveis
            self.cur.execute(
                "SELECT quantidade_assentos FROM voos WHERE sigla = %s;",
                (sigla,)
            )
            result = self.cur.fetchone()

            if result is None:
                return "Voo não encontrado."

            quantidade_assentos = result[0]

            if quantidade_assentos <= 0:
                return "Não há assentos disponíveis."

            # Atualizar quantidade de assentos disponíveis
            self.cur.execute(
                "UPDATE voos SET quantidade_assentos = quantidade_assentos - 1 WHERE sigla = %s;",
                (sigla,)
            )
            self.conn.commit()
            return "Reserva confirmada!"
        except Exception as e:
            print(f"Erro ao reservar voo: {e}")
            return "Erro ao realizar a reserva."

    def close_connection(self):
        self.cur.close()
        self.conn.close()


class BackendRemoverReservas:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',
                user='poodois',
                password='1234',
                host='localhost',
                port=5432
            )
            self.cur = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_table(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS voos (
                    id SERIAL PRIMARY KEY,
                    sigla TEXT NOT NULL,
                    origem TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    modelo_aviao TEXT NOT NULL,
                    quantidade_assentos INTEGER NOT NULL
                );
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

    def listar_voos(self):
        try:
            self.cur.execute("SELECT sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
            voos = self.cur.fetchall()
            return voos
        except Exception as e:
            print(f"Erro ao listar voos: {e}")
            return []

    def remover_reserva_voo(self, sigla, assento):
        try:
            # Verificar se o voo existe e há assentos disponíveis
            self.cur.execute(
                "SELECT quantidade_assentos FROM voos WHERE sigla = %s;",
                (sigla,)
            )
            result = self.cur.fetchone()

            if result is None:
                return "Voo não encontrado."

            quantidade_assentos = result[0]

            if quantidade_assentos <= 0:
                return "Não há assentos disponíveis."

            # Atualizar quantidade de assentos disponíveis
            self.cur.execute(
                "UPDATE voos SET quantidade_assentos = quantidade_assentos + 1 WHERE sigla = %s;",
                (sigla,)
            )
            self.conn.commit()
            return "Reserva confirmada!"
        except Exception as e:
            print(f"Erro ao reservar voo: {e}")
            return "Erro ao realizar a reserva."

    def close_connection(self):
        self.cur.close()
        self.conn.close()

class MetodosGerente:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='credenciais',  # Nome do banco de dados
                user='poodois',        # Nome do usuário
                password='1234',       # Senha do usuário
                host='localhost',
                port=5432
            )

            self.criar_tabela()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        """Cria a tabela de aviões caso não exista."""
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS avioes (
                    id SERIAL PRIMARY KEY,
                    sigla TEXT UNIQUE NOT NULL,
                    modelo TEXT NOT NULL,
                    assentos INTEGER NOT NULL
                );
            ''')
            self.conn.commit()

    def cadastrar_aviao(self, sigla: str, modelo: str, assentos: int) -> tuple:
        """Insere ou atualiza os dados de um avião no banco de dados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    sql.SQL('''
                        INSERT INTO avioes (sigla, modelo, assentos)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (sigla) DO UPDATE
                        SET modelo = EXCLUDED.modelo, assentos = EXCLUDED.assentos;
                    '''),
                    (sigla, modelo, assentos)
                )
                self.conn.commit()
            return True, "Avião cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar avião: {str(e)}"

    def listar_avioes(self):
        """Retorna uma lista com todos os aviões cadastrados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, modelo, assentos FROM avioes;")
                avioes = cur.fetchall()
            return avioes
        except Exception as e:
            return []

    def buscar_aviao_por_sigla(self, sigla: str) -> tuple:
        """Busca um avião pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, sigla, modelo, assentos FROM avioes WHERE sigla = %s;",
                    (sigla,)
                )
                aviao = cur.fetchone()
            if aviao:
                return aviao
            return None
        except Exception as e:
            return None

    def excluir_aviao(self, sigla: str) -> tuple:
        """Exclui um avião pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM avioes WHERE sigla = %s;",
                    (sigla,)
                )
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Avião excluído com sucesso."
                return False, "Avião não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir avião: {str(e)}"
    
    def alterar_aviao(self, sigla: str, novo_modelo: str, novos_assentos: int) -> tuple:
        """Altera os dados de um avião existente no banco de dados."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE avioes 
                    SET modelo = %s, assentos = %s 
                    WHERE sigla = %s;
                    ''',
                    (novo_modelo, novos_assentos, sigla)
                )
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Avião atualizado com sucesso."
                return False, "Avião não encontrado."
        except Exception as e:
            return False, f"Erro ao alterar avião: {str(e)}"
