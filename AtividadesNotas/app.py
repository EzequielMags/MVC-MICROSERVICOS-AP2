from flask import Flask, Blueprint
from flasgger import Swagger
from config import Config
import requests
from requests.adapters import HTTPAdapter, Retry
from controllers.atividades_controllers import AtividadesController
from controllers.notas_controllers import NotasController
from models import db

app = Flask(__name__)
app.config.from_object(Config)
Config.ensure_instance_dir_exists()
swagger = Swagger(app)

def http_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

def get_turma(turma_id: int):
   url = f"http://gerenciamento:5000/turmas/{turma_id}"
   response = http_session().get(url, timeout=10)
   response.raise_for_status()
   return response.json()

def get_professor(professor_id: int):
   url = f"http://gerenciamento:5000/professores/{professor_id}"
   response = http_session().get(url, timeout=10)
   response.raise_for_status()
   return response.json()

def get_aluno(aluno_id: int):
   url = f"http://gerenciamento:5000/alunos/{aluno_id}"
   response = http_session().get(url, timeout=10)
   response.raise_for_status()
   return response.json()

def get_atividade(atividade_id: int):
   url = f"http://atividadesnotas:5001/atividades/{atividade_id}"
   response = http_session().get(url, timeout=10)
   response.raise_for_status()
   return response.json()


db.init_app(app)


with app.app_context():
    db.create_all()

# Blueprints de Atividades
atividades_bp = Blueprint('atividades', __name__)
atividades_bp.route('/', methods=['GET'])(AtividadesController.listar_atividades)
atividades_bp.route('/<int:atividade_id>', methods=['GET'])(AtividadesController.buscar_atividade_por_id)
atividades_bp.route('/', methods=['POST'])(AtividadesController.criar_atividade)
atividades_bp.route('/<int:atividade_id>', methods=['PUT'])(AtividadesController.atualizar_atividade)
atividades_bp.route('/<int:atividade_id>', methods=['DELETE'])(AtividadesController.deletar_atividade)
app.register_blueprint(atividades_bp, url_prefix='/atividades')

# Blueprints de Notas
notas_bp = Blueprint('notas', __name__)
notas_bp.route('/', methods=['GET'])(NotasController.listar_notas)
notas_bp.route('/<int:nota_id>', methods=['GET'])(NotasController.buscar_nota_por_id)
notas_bp.route('/', methods=['POST'])(NotasController.criar_nota)
notas_bp.route('/<int:nota_id>', methods=['PUT'])(NotasController.atualizar_nota)
notas_bp.route('/<int:nota_id>', methods=['DELETE'])(NotasController.deletar_nota)
app.register_blueprint(notas_bp, url_prefix='/notas')



@app.route('/health')
def health():
    return {'status': 'ok'}, 200
                       
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)