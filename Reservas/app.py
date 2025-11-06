from flask import Flask, jsonify,Blueprint
from controllers.reservas_controllers import ReservasController
import requests
from requests.adapters import HTTPAdapter, Retry
from flasgger import Swagger
from config import Config
from models import db


app = Flask(__name__)
app.config.from_object(Config)
Config.ensure_instance_dir_exists()
swagger = Swagger(app)
db.init_app(app)

with app.app_context():
    db.create_all()
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
        
# Blueprint de Reservas
reservas_bp = Blueprint('reservas', __name__)
reservas_bp.route('/', methods=['GET'])(ReservasController.listar_reservas)
reservas_bp.route('/<int:reserva_id>', methods=['GET'])(ReservasController.buscar_reserva_por_id)
reservas_bp.route('/', methods=['POST'])(ReservasController.criar_reserva)
reservas_bp.route('/<int:reserva_id>', methods=['PUT'])(ReservasController.atualizar_reserva)
reservas_bp.route('/<int:reserva_id>', methods=['DELETE'])(ReservasController.deletar_reserva)
app.register_blueprint(reservas_bp, url_prefix='/reservas')

@app.route('/health')
def health():
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)