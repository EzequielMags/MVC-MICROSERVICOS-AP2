from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy para ser usada por todos os modelos
db = SQLAlchemy()

# Importar todos os modelos para garantir que sejam registrados
from .atividades import Atividades
from .notas import Notas

# Lista de todos os modelos para facilitar a criação das tabelas
__all__ = ['db', 'Atividades', 'Notas']