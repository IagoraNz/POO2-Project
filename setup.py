from setuptools import setup, find_packages

setup(
    name="listar_clientes",  # Nome da biblioteca
    version="0.1.0",  # Versão atual da biblioteca
    description="Biblioteca para listar todos os clientes cadastrados no PostGreSQL",  # Descrição breve do que a biblioteca faz
    author="Daniel, Francinaldo, Luis, Rita, Iago, Cristina",  # Lista de autores da biblioteca
    packages=find_packages(),  # Encontrar todos os pacotes da biblioteca para incluir na distribuição
    install_requires=[  # Dependências que serão instaladas automaticamente
        "psycopg2",  # Dependência para conectar com o Redis
    ],
    python_requires=">=3.9.13",  # Especifica a versão mínima do Python necessária
)