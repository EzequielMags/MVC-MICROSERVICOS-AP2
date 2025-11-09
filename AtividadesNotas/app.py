from flask import Flask, Blueprint
from flasgger import Swagger
from config import Config
import requests
from controllers.atividades_controllers import AtividadesController
from controllers.notas_controllers import NotasController
from models import db

app = Flask(__name__)
app.config.from_object(Config)
Config.ensure_instance_dir_exists()
swagger = Swagger(app)









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