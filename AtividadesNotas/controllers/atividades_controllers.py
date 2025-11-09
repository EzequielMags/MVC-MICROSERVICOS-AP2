from flask import request, jsonify
import requests
from models import db
from models.atividades import Atividades
from flasgger import swag_from
from datetime import datetime

def get_turma(turma_id: int):
    try:
        response = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
        if response.status_code == 200:
            return response.json()  # retorna os dados da turma
        return None  # turma não encontrada
    except requests.RequestException as e:
        print(f"Erro ao buscar turma: {e}")
        return None


# Função para buscar professor no serviço de gerenciamento
def get_professor(professor_id: int):
    try:
        response = requests.get(f"http://gerenciamento:5000/professores/{professor_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"Erro ao buscar professor: {e}")
        return None

class AtividadesController:

    @staticmethod
    @swag_from({
        'tags': ['Atividades'],
        'summary': 'Listar todas as atividades',
        "responses": {
            '200': {
                'description': 'Lista de atividades retornada com sucesso',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'nome_atividade': "atividade de matematica",
                                'descricao': 'teste de descricao',
                                'peso_porcento': 20,
                                'data_entrega': '2009-03-10',
                                'professor_id': 1,
                                'turma_id': 1 
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_atividades():
        atividades = Atividades.query.order_by(Atividades.id.asc()).all()
        atividades_list = [atividade.to_dict() for atividade in atividades]
        return jsonify(atividades_list), 200
    
    @staticmethod
    @swag_from({
        'tags': ['Atividades'],
        'summary': 'Buscar atividade por ID',
        "parameters": [
            {
                "name": "atividade_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID da atividade a ser buscada"
            }
        ],  
          'responses': {
            '200': {'description': 'Atividade encontrada'},
            '404': {'description': 'Atividade não encontrada'}
        }
    })
    def buscar_atividade_por_id(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if atividade:
            return jsonify(atividade.to_dict()), 200
        else:
            return jsonify({'message': 'Atividade não encontrada'}), 404    

    @staticmethod
    @swag_from({
        'tags': ['Atividades'],
        'summary': 'Criar uma nova atividade',
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "nome_atividade": {"type": "string"},
                            "descricao": {"type": "string"},
                            "peso_porcento": {"type": "integer"},
                            "data_entrega": {"type": "string", "format": "date"},
                            "professor_id": {"type": "integer"},
                            "turma_id": {"type": "integer"}
                        },
                        "required": ["nome_atividade", "descricao", "peso_porcento", "data_entrega", "professor_id", "turma_id"]
                    }
                }
            }
        },
        "responses": {
            '201': {'description': 'Atividade criada com sucesso'}
        }
    })
    def criar_atividade():
        data = request.get_json()
        # Converter data_entrega string (YYYY-MM-DD) para date
        data_entrega_str = data.get('data_entrega')
        
        turma = get_turma(data["turma_id"])

        if not turma:
            return jsonify({'message': 'turma não encontrada'}), 400

        professor = get_professor(data["professor_id"])

        if not professor: 
            return jsonify({"message": "professor não encontrado"}), 400

        data_entrega = None
        if data_entrega_str:
            try:
                data_entrega = datetime.strptime(data_entrega_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'data_entrega deve estar no formato YYYY-MM-DD'}), 400
        nova_atividade = Atividades(
            id=data['id'],
            nome_atividade=data['nome_atividade'],
            descricao=data['descricao'],
            peso_porcento=data['peso_porcento'],
            data_entrega=data_entrega,
            professor_id=data['professor_id'],
            turma_id=data['turma_id']
        )
        db.session.add(nova_atividade)
        db.session.commit()
        return jsonify(nova_atividade.to_dict()), 201

    @staticmethod
    @swag_from({
        'tags': ['Atividades'],
        'summary': 'Atualizar uma atividade existente',
        "parameters": [
            {
                "name": "atividade_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID da atividade a ser atualizada"
            }
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "nome_atividade": {"type": "string"},
                            "descricao": {"type": "string"},
                            "peso_porcento": {"type": "integer"},
                            "data_entrega": {"type": "string", "format": "date"},
                            "professor_id": {"type": "integer"},
                            "turma_id": {"type": "integer"}
                        }
                    }
                }
            }
        },
        "responses": {
            '200': {'description': 'Atividade atualizada com sucesso'},
            '404': {'description': 'Atividade não encontrada'}
        }
    })
    def atualizar_atividade(atividade_id):
        data = request.get_json()
        atividade = Atividades.query.get(atividade_id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404

        atividade.id = data.get('id', atividade.id)
        atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
        atividade.descricao = data.get('descricao', atividade.descricao)
        atividade.peso_porcento = data.get('peso_porcento', atividade.peso_porcento)
        if 'data_entrega' in data and data['data_entrega'] is not None:
            try:
                atividade.data_entrega = datetime.strptime(data['data_entrega'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'data_entrega deve estar no formato YYYY-MM-DD'}), 400
        atividade.professor_id = data.get('professor_id', atividade.professor_id)
        atividade.turma_id = data.get('turma_id', atividade.turma_id)

        db.session.commit()
        db.session.refresh(atividade)
        return jsonify(atividade.to_dict()), 200

    @staticmethod
    @swag_from({
        'tags': ['Atividades'],
        'summary': 'Deletar uma atividade',
        "parameters": [
            {
                "name": "atividade_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID da atividade a ser deletada"
            }
        ],
        "responses": {
            '200': {'description': 'Atividade deletada com sucesso'},
            '404': {'description': 'Atividade não encontrada'}
        }
    })
    def deletar_atividade(atividade_id):
        atividade = Atividades.query.get(atividade_id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404

        db.session.delete(atividade)
        db.session.commit()
        return jsonify({'message': 'Atividade deletada com sucesso'}), 200
        