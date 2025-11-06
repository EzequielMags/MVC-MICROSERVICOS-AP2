import os
from pathlib import Path

class Config:
    # Configuração do banco de dados SQLite
    basedir = Path(__file__).parent
    # Caminhos calculados sem efeitos colaterais em import
    instance_dir = (basedir / 'instance')
    db_path = (instance_dir / 'database.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Configurações de desenvolvimento
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = True

    @staticmethod
    def ensure_instance_dir_exists() -> None:
        # Cria a pasta somente em tempo de inicialização do app
        Config.instance_dir.mkdir(parents=True, exist_ok=True)