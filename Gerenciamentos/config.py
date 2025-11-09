import os
from pathlib import Path

class Config:
    # Configuração do banco de dados SQLite
    basedir = Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Configurações de desenvolvimento
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = True