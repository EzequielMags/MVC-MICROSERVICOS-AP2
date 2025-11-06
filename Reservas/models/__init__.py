from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy para ser usada por todos os modelos
db = SQLAlchemy()

# Importar o modelo principal deste serviço
from .reservas import Reservas

# Lista de todos os modelos para facilitar a criação das tabelas
__all__ = ['db', 'Reservas']