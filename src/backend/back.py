from psycopg2 import sql
import psycopg2

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