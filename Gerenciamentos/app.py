import os 
from flask import Flask
from flask import Blueprint
from flasgger import Swagger
from config import Config
from controllers.professor_controllers import ProfessorController
from controllers.turma_controllers import TurmaController
from controllers.aluno_controllers import AlunoController
from models import db

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

swagger = Swagger(app)

db.init_app(app)

with app.app_context():
    db.create_all()


#ROTAS DE ALUNO
aluno_bp = Blueprint('aluno_bp', __name__, url_prefix='/alunos')
aluno_bp.route('/', methods=['GET'])(AlunoController.listar_alunos)
aluno_bp.route('/', methods=['POST'])(AlunoController.criar_aluno)
aluno_bp.route('/<int:id>', methods=['GET'])(AlunoController.buscar_aluno)
aluno_bp.route('/<int:id>', methods=['PUT'])(AlunoController.atualizar_aluno)
aluno_bp.route('/<int:id>', methods=['DELETE'])(AlunoController.deletar_aluno)
app.register_blueprint(aluno_bp)

#ROTAS DE PROFESSOR
professor_bp = Blueprint('professor_bp', __name__, url_prefix='/professores')
professor_bp.route('/', methods=['GET'])(ProfessorController.listar_professores)
professor_bp.route('/', methods=['POST'])(ProfessorController.criar_professor)
professor_bp.route('/<int:id>', methods=['GET'])(ProfessorController.buscar_professor)
professor_bp.route('/<int:id>', methods=['PUT'])(ProfessorController.atualizar_professor)
professor_bp.route('/<int:id>', methods=['DELETE'])(ProfessorController.deletar_professor)
app.register_blueprint(professor_bp)

#ROTAS DE TURMA
turma_bp = Blueprint('turma_bp', __name__, url_prefix='/turmas')
turma_bp.route('/', methods=['GET'])(TurmaController.listar_turmas)
turma_bp.route('/', methods=['POST'])(TurmaController.criar_turma)
turma_bp.route('/<int:id>', methods=['GET'])(TurmaController.buscar_turma)
turma_bp.route('/<int:id>', methods=['PUT'])(TurmaController.atualizar_turma)
turma_bp.route('/<int:id>', methods=['DELETE'])(TurmaController.deletar_turma)
app.register_blueprint(turma_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)