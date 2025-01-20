import psycopg2
from psycopg2 import sql

class ListarClientes:
    def __init__(self, db_config):
        """
        Inicializa a classe com uma configuração de banco de dados.

        :param db_config: Dicionário contendo informações para conectar ao banco de dados.
                         Exemplo: {
                             'dbname': 'credenciais',
                             'user': 'poodois',
                             'password': '1234',
                             'host': 'localhost',
                             'port': 5432
                         }
        """
        self.db_config = db_config
        self.conn = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None

    def listar_clientes(self):
        """Retorna uma lista com todos os clientes cadastrados."""
        if not self.conn:
            print("Conexão com o banco de dados não está disponível.")
            return []

        try:
            with self.conn.cursor() as cur:
                query = sql.SQL("SELECT id, nome, cpf, telefone FROM clientes;")
                cur.execute(query)
                clientes = cur.fetchall()
                return clientes
        except psycopg2.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []

    def __del__(self):
        """Garante que a conexão seja fechada ao destruir o objeto."""
        if self.conn:
            self.conn.close()
