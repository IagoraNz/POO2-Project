import psycopg2
from psycopg2 import sql

class ListarClientes:
    """
    Summary:
        Classe que lista os clientes cadastrados no banco de dados.
        
    Attributes:
        db_config: Dicionário contendo informações para conectar ao banco de dados.
        
    Methods:
        connect: Estabelece a conexão com o banco de dados.
    """
    def __init__(self, db_config) -> None:
        """
        Summary:
            Inicializa a classe com uma configuração de banco de dados.

        Args:
            db_config: Dicionário contendo informações para conectar ao banco de dados.
            
        Returns:
            None
        """
        self.db_config = db_config
        self.conn = None
        self.connect()

    def connect(self) -> None:
        """
        Summary:
            Estabelece a conexão com o banco de dados.
        
        Args:
            None
        
        Returns:
            None
            
        Raises:
            psycopg2.Error: Erro ao conectar ao banco de dados.
        """
        try:
            self.conn = psycopg2.connect(**self.db_config)
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None

    def listar_clientes(self) -> list:
        """
        Summary:
            Retorna uma lista com todos os clientes cadastrados.
        
        Args:
            None
            
        Returns:
            list: Lista contendo os clientes cadastrados.
            
        Raises:
            psycopg2.Error: Erro ao executar a consulta no banco de dados.
        """
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

    def __del__(self) -> None:
        """
        Summary:
            Garante que a conexão seja fechada ao destruir o objeto.
        
        Args:
            None
            
        Returns:
            None
        """
        if self.conn:
            self.conn.close()
