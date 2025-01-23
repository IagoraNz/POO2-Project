from psycopg2 import sql
import psycopg2

class Aviao():
    """
    Classe que representa um avião.
    """
    def __init__(self, modelo: str, quantidade_assentos: int, sigla_av: str) -> None: 
        """
        Inicializa a classe Aviao.

        Args:
            modelo: (str) Modelo do avião.
            quantidade_assentos: (int) Quantidade de assentos disponíveis.
            sigla_av: (str) Sigla identificadora do avião.
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
    """
    def __init__(self, sigla: str, origem: str, destino: str, aviao: object) -> None:
        """
        Inicializa a classe Voo.

        Args:
            sigla: (str) Identificador do voo.
            origem: (str) Cidade de origem.
            destino: (str) Cidade de destino.
            aviao: (Aviao) Avião utilizado no voo.
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
        
    def preenche_assentos(self, quantidade: int) -> tuple [bool|str]:
        """
        Preenche a lista de assentos disponíveis no voo.

        Args:
            quantidade: (int) Quantidade de assentos a preencher.

        Returns:
            tuple: (bool, str) indicando o sucesso e uma mensagem.
        """
        for i in range(i, quantidade - 1):
            self._assentos.append(i)
        return True, 'Assentos preenchidos com sucesso'
    
    def reservar_assento(self, numero: int) -> tuple [bool|str]:
        """
        Reserva um assento no voo.

        Args:
            numero: (int) Número do assento a ser reservado.

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
    
    """
    def __init__(self, nome: str, cpf: int, telefone: int) -> None:
        """
        Inicializa a classe Passageiro.

        Args:
            nome: (str) Nome do passageiro.
            cpf: (int) CPF do passageiro.
            telefone: (int) Número de telefone do passageiro.
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
            nome: (str) Nome do funcionário.
            cpf: (int) CPF do funcionário.
            salario: (float) Salário do funcionário.
            senha: (str) Senha do funcionário.
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
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, expediente: str) -> None:
        """
        Inicializa um objeto Gerente.

        Args:
            nome: (str) Nome do gerente.
            cpf: (int) CPF do gerente.
            salario: (float) Salário do gerente.
            senha: (str) Senha do gerente.
            expediente: (str) Horário de expediente do gerente.
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
    def __init__(self, nome: str, cpf: int, salario: float, senha: str, terminal: int) -> None:
        """
        Inicializa um objeto Atendente.

        Args:
            nome: (str) Nome do atendente.
            cpf: (int) CPF do atendente.
            salario: (float) Salário do atendente.
            senha: (str) Senha do atendente.
            terminal: (int) Terminal atribuído ao atendente.
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
    def __init__(self, user: str, senha: str) -> None:
        """
        Inicializa um objeto Autenticacao.

        Args:
            user: (str) Nome de usuário.
            senha: (str) Senha do usuário.
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

    def cadastro(self, user: str, senha: str, tipo: int) -> tuple[bool|str]:
        """
        Cadastra ou atualiza um usuário no banco de dados.

        Args:
            user: (str) Nome de usuário.
            senha: (str) Senha do usuário.
            tipo: (int) Tipo de usuário (1 para gerente, 2 para atendente).

        Returns:
            tuple: (bool|str) Status e mensagem de sucesso ou erro.
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
        Realiza o login de um usuário.

        Args:
            user: (str) Nome de usuário.
            senha: (str) Senha do usuário.

        Returns:
            tuple: (bool|str) Status e mensagem indicando o tipo de usuário ou erro.
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
    def __init__(self, nome: str, cnpj: int, telefone: int, endereco: str) -> None:
        """
        Inicializa um objeto CiaAerea.

        Args:
            nome: (str) Nome da companhia aérea.
            cnpj: (int) CNPJ da companhia aérea.
            telefone: (int) Telefone da companhia aérea.
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
        
    def add_aviao(self, aviao: object) -> tuple[bool|str]:
        """
        Adiciona um avião à companhia aérea.

        Args:
            aviao: (object) Objeto da classe Aviao.

        Returns:
            tuple:(bool|str) Status e mensagem indicando sucesso ou erro.
        """
        if isinstance(aviao, Aviao):
            if aviao._sigla_av not in self._avioes.keys():
                self._avioes[aviao.sigla_av] = aviao
                return True, 'Avião cadastrado com sucesso!'
            return False, 'Avião já cadastrado!'
        return False, 'Avião inválido!'
    
    def excluir_aviao(self, sigla: str) -> tuple[bool|str]:
        """
        Exclui um avião do sistema.

        Args:
            sigla: (str) A sigla identificadora do avião.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if sigla in self._avioes.keys():
            del self._avioes[sigla]
            return True, 'Avião excluído com sucesso!'
        return False, 'Avião não encontrado!'

    def add_voo(self, voo: object) -> tuple [bool|str]:
        """
        Adiciona um voo ao sistema.

        Args:
            voo: (object) Objeto do tipo `Voo` representando o voo a ser adicionado.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if isinstance(voo, Voo):
            if voo.sigla not in self._voos:
                self._voos[voo.sigla] = voo
                return True, 'Voo cadastrado com sucesso!'
            return False, 'Voo já cadastrado!'
        return False, 'Voo inválido!'
    
    def excluir_voo(self, sigla: str) -> tuple[bool|str]:
        """
        Exclui um voo do sistema.

        Args:
            sigla: (str) A sigla identificadora do voo.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if sigla in self._voos.keys():
            del self._voos[sigla]
            return True, 'Voo excluído com sucesso!'
        return False, 'Voo não encontrado!'
    
    def add_passageiro(self, passageiro: object) -> tuple[bool|str]:
        """
        Adiciona um passageiro ao sistema.

        Args:
            passageiro: (object) Objeto do tipo `Passageiro` representando o passageiro.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if isinstance(passageiro, Passageiro):
            if passageiro.cpf not in self._passageiros:
                self._passageiros[passageiro.cpf] = passageiro
                return True, 'Passageiro cadastrado com sucesso!'
            return False, 'Passageiro já cadastrado!'
        return False, 'Passageiro inválido!'
    
    def excluir_passageiro(self, cpf: int) -> tuple[bool|str]:
        """
        Exclui um passageiro do sistema.

        Args:
            cpf: (int) O CPF do passageiro.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if cpf in self._passageiros.keys():
            del self._passageiros[cpf]
            return True, 'Passageiro excluído com sucesso!'
        return False, 'Passageiro não encontrado!'
    
    def add_funcionario(self, funcionario: object) -> tuple[bool|str]:
        """
        Adiciona um funcionário ao sistema.

        Args:
            funcionario: (object) Objeto do tipo `Funcionario` representando o funcionário.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if isinstance(funcionario, Funcionario):
            if funcionario.cpf not in self._funcionarios:
                self._funcionarios[funcionario.cpf] = funcionario
                return True, "Funcionário cadastrado com sucesso!"
            return False, "Funcionário já cadastrado!"
        return False, "Funcionário inválido!"
    
    def excluir_funcionario(self, cpf: object) -> tuple[bool|str]:
        """
        Exclui um funcionário do sistema.

        Args:
            cpf: (int) O CPF do funcionário.

        Returns:
            tuple: (bool, str) indicando o sucesso da operação e uma mensagem.
        """
        if cpf in self._funcionarios.keys():
            del self._funcionarios[cpf]
            return True, "Funcionário excluído com sucesso!"
        return False, "Funcionário não encontrado!"
    

class CadastroClientes:
    """
    Classe responsável por gerenciar o cadastro de clientes em um banco de dados PostgreSQL.
    """
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e cria a tabela de clientes se ela não existir.
        
        Raises:
            ConnectionError: Caso ocorra um erro ao conectar ao banco de dados.
        """
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

    def cadastrar_cliente(self, nome: str, cpf: str, telefone: str) -> tuple[bool|str]:
        """
        Insere ou atualiza os dados de um cliente no banco de dados.

        Args:
            nome: (str) Nome do cliente.
            cpf: (str) CPF do cliente.
            telefone: (str) Telefone do cliente.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
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


    def buscar_cliente_por_cpf(self, cpf: str) -> tuple[bool|str]:
        """
        Busca um cliente no banco de dados pelo CPF.

        Args:
            cpf (str): CPF do cliente.

        Returns:
            tuple: (bool|str) Uma tupla contendo os dados do cliente (id, nome, cpf, telefone), 
                   ou None caso o cliente não seja encontrado.
        """
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

    def excluir_cliente(self, cpf: str) -> tuple[bool|str]:
        """
        Exclui um cliente do banco de dados pelo CPF.

        Args:
            cpf: (str) CPF do cliente a ser excluído.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
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
    
    def alterar_cliente(self, cpf: str, novo_nome: str, novo_telefone: str) -> tuple[bool|str]:
        """
        Altera os dados de um cliente existente no banco de dados pelo CPF.

        Args:
            cpf: (str) CPF do cliente a ser alterado.
            novo_nome: (str) Novo nome do cliente.
            novo_telefone: (str) Novo telefone do cliente.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
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
    """
    Classe responsável por gerenciar o cadastro de voos em um banco de dados PostgreSQL.
    """
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e cria a tabela de voos, caso não exista.
        
        Raises:
            ConnectionError: Caso ocorra um erro ao conectar ao banco de dados.
        """
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

    def cadastrar_voo(self, sigla: str, origem: str, destino: str, modelo_aviao: str, quantidade_assentos: int) -> tuple[bool|str]:
        """
        Insere os dados de um voo no banco de dados.

        Args:
            sigla: (str) Identificação única do voo (exemplo: código do voo).
            origem: (str) Local de origem do voo.
            destino: (str) Local de destino do voo.
            modelo_aviao: (str) Modelo do avião.
            quantidade_assentos: (int) Quantidade total de assentos disponíveis no avião.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    '''
                    INSERT INTO voos (sigla, origem, destino, modelo_aviao, quantidade_assentos)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (sigla, origem, destino, modelo_aviao, quantidade_assentos)
                )
                self.conn.commit()
            return True, "Voo cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar voo: {str(e)}"

    def listar_voos(self) -> list[tuple]:
        """"
        Returns:
            list: Uma lista contendo tuplas com os dados de cada voo.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
                voos = cur.fetchall()
            return voos
        except Exception as e:
            return []

    def buscar_voo_por_sigla(self, sigla: str) -> tuple[int, str, str, str, str]:
        """
        Busca os dados de um voo no banco de dados pela sigla.

        Args:
            sigla: (str) Identificação única do voo.

        Returns:
            tuple: Uma tupla contendo os dados do voo (id, sigla, origem, destino, modelo_aviao),
                   ou None caso o voo não seja encontrado.
        """
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

    def excluir_voo(self, sigla: str) -> tuple[bool|str]:
        """
        Exclui um voo do banco de dados pela sigla.

        Args:
            sigla: (str) Identificação única do voo a ser excluído.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
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

    def alterar_voo(self, sigla: str, origem: str, destino: str, modelo_aviao: str, quantidade_assentos: int) -> tuple[bool|str]:
        """
        Altera os dados de um voo existente no banco de dados pela sigla.

        Args:
            sigla: (str) Identificação única do voo a ser alterado.
            origem: (str) Novo local de origem do voo.
            destino: (str) Novo local de destino do voo.
            modelo_aviao: (str) Novo modelo do avião.
            quantidade_assentos: (int) Nova quantidade total de assentos disponíveis.

        Returns:
            tuple: Um par (bool, str), onde o bool indica sucesso (True) ou falha (False),
                   e a string contém uma mensagem descritiva.
        """
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
    
    def buscar_assentos_por_aviao(self, sigla_aviao: str) -> int:
        """Busca a quantidade de assentos de um avião pelo campo sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT assentos FROM avioes WHERE sigla = %s;",
                    (sigla_aviao,)
                )
                result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            return None


class BackendReservas:
    """
    Classe responsável por gerenciar reservas de voos em um banco de dados PostgreSQL.
    """

    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e cria a tabela de voos, se não existir.
        """
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
        """
        Cria a tabela de voos no banco de dados, caso ela ainda não exista.
        """
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

    def listar_voos(self) -> list[tuple]:
        """
        Lista todos os voos disponíveis no banco de dados.

        Returns:
            list: Lista de tuplas contendo os dados dos voos.
        """
        try:
            self.cur.execute("SELECT sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
            voos = self.cur.fetchall()
            return voos
        except Exception as e:
            print(f"Erro ao listar voos: {e}")
            return []

    def reservar_voo(self, sigla: str, assento: int) -> str:
        """
        Realiza a reserva de um assento para um voo específico.

        Args:
            sigla: (str) Sigla do voo a ser reservado.
            assento: (int) Número do assento a ser reservado.

        Returns:
            str: Mensagem indicando o status da reserva.
        """
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
        """
        Fecha a conexão com o banco de dados.
        """
        self.cur.close()
        self.conn.close()


class BackendRemoverReservas:
    """
    Classe para gerenciar remoção de reservas de voos no banco de dados.
    
    Atributos:
        conn (psycopg2.connection): Conexão com o banco de dados.
        cur (psycopg2.cursor): Cursor para executar comandos SQL.
    """
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e cria a tabela de voos, se não existir.

        Raises:
            Exception: Erro ao conectar ao banco de dados.
        """
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
        """
        Cria a tabela de voos no banco de dados, caso não exista.
        """
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
        """
        Lista todos os voos cadastrados no banco de dados.
        
        Returns:
            list: Lista de tuplas contendo os dados dos voos (sigla, origem, destino, modelo_aviao, quantidade_assentos).
        """
        try:
            self.cur.execute("SELECT sigla, origem, destino, modelo_aviao, quantidade_assentos FROM voos;")
            voos = self.cur.fetchall()
            return voos
        except Exception as e:
            print(f"Erro ao listar voos: {e}")
            return []

    def remover_reserva_voo(self, sigla: str, assento: int) -> str:
        """
        Remove a reserva de um assento para um voo específico.

        Args:
            sigla: (str) Sigla do voo cuja reserva será removida.
            assento: (int) Número do assento a ser removido.

        Returns:
            str: Mensagem indicando o status da remoção.
        """
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
        """
        Fecha a conexão com o banco de dados.
        """
        self.cur.close()
        self.conn.close()

class MetodosGerente:
    """
    Classe responsável por gerenciar aviões em um banco de dados PostgreSQL.
    
    Atributos:
        conn: Conexão com o banco de dados PostgreSQL.
    """
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e cria a tabela de aviões se ela não existir.
        
        Raise:
            ConnectionError: Se ocorrer um erro ao conectar ao banco de dados.
        """
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

    def cadastrar_aviao(self, sigla: str, modelo: str, assentos: int) -> tuple[bool|str]:
        """
        Insere ou atualiza os dados de um avião no banco de dados.

        Parâmetros:
            sigla: (str) Código único do avião.
            modelo: (str) Modelo do avião.
            assentos: (int) Número de assentos do avião.

        Retorno:
            tuple[bool, str]: 
                - `True` e mensagem de sucesso se o avião foi cadastrado ou atualizado com sucesso.
                - `False` e mensagem de erro em caso de falha.
        """
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

    def listar_avioes(self) -> list[tuple]:
        """
        Retorna uma lista com todos os aviões cadastrados.

        Retorno:
            list[tuple]: Lista contendo os aviões no formato 
                         (id, sigla, modelo, assentos). 
                         Retorna uma lista vazia em caso de erro.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, modelo, assentos FROM avioes;")
                avioes = cur.fetchall()
            return avioes
        except Exception as e:
            return []

    def buscar_aviao_por_sigla(self, sigla: str) -> tuple | None:
        """Busca um avião pela sigla.
        
         Parâmetros:
            sigla: (str) Código único do avião.

        Retorno:
            tuple | None:
                - Um tupla contendo (id, sigla, modelo, assentos) se o avião for encontrado.
                - `None` se o avião não existir ou em caso de erro.
        """
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

    def excluir_aviao(self, sigla: str) -> tuple[bool, str]:
        """Exclui um avião pela sigla.
         Parâmetros:
            sigla: (str) Código único do avião a ser excluído.

        Retorno:
            tuple[bool, str]: 
                - `True` e mensagem de sucesso se o avião foi excluído.
                - `False` e mensagem de erro ou avião não encontrado.
        """
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
    
    def alterar_aviao(self, sigla: str, novo_modelo: str, novos_assentos: int) -> tuple[bool|str]:
        """Altera os dados de um avião existente no banco de dados.
            Parâmetros:
                sigla: (str) Código único do avião.
                novo_modelo: (str) Novo modelo do avião.
                novos_assentos: (int) Novo número de assentos.

            Retorno:
                tuple[bool, str]: 
                    - `True` e mensagem de sucesso se o avião foi atualizado.
                    - `False` e mensagem de erro ou avião não encontrado.
        """
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