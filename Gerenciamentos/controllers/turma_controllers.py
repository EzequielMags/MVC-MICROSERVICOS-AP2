from flask import request, jsonify
from models.turma import Turma
from models import db
from flasgger import swag_from
import requests

def get_professor(professor_id: int):
    try:
        response = requests.get(f"http://gerenciamento:5000/professores/{professor_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"Erro ao buscar professor: {e}")
        return None

class TurmaController:

    @staticmethod
    @swag_from({
        'tags': ['Turmas'],
        'summary': 'Lista todas as turmas',
        'responses': {
            '200': {
                'description': 'Lista de turmas',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'descricao': '1º Ano A',
                                'professor_id': 3,
                                'ativo': True
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_turmas():
        turmas = Turma.query.all()
        return jsonify([
            {
                'id': t.id,
                'descricao': t.descricao,
                'professor_id': t.professor_id,
                'ativo': t.ativo
            } for t in turmas
        ]), 200

    @staticmethod
    @swag_from({
        'tags': ['Turmas'],
        'summary': 'Cria uma nova turma',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'descricao': {'type': 'string'},
                            'professor_id': {'type': 'integer'},
                            'ativo': {'type': 'boolean'}
                        },
                        'required': ['descricao', 'professor_id', 'ativo']
                    },
                    'example': {
                        'descricao': '1º Ano A',
                        'professor_id': 3,
                        'ativo': True
                    }
                }
            }
        },
        'responses': {
            '201': {'description': 'Turma criada com sucesso'},
            '400': {'description': 'Dados inválidos'}
        }
    })
    def criar_turma():
        data = request.get_json(silent=True) or {}

        descricao = data.get('descricao')
        professor_id = data.get('professor_id')

        professor = get_professor(data["professor_id"])

        if not professor:
            return jsonify({'message': 'professor não encontrada'}), 400

        ativo = data.get('ativo')

        if descricao is None or professor_id is None or ativo is None:
            return jsonify({'error': 'descricao, professor_id e ativo são obrigatórios'}), 400

        turma = Turma(
            descricao=descricao,
            professor_id=professor_id,
            ativo=ativo
        )
        db.session.add(turma)
        db.session.commit()

        return jsonify({
            'id': turma.id,
            'descricao': turma.descricao,
            'professor_id': turma.professor_id,
            'ativo': turma.ativo
        }), 201

    @staticmethod
    @swag_from({
        'tags': ['Turmas'],
        'summary': 'Busca uma turma por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '200': {'description': 'Turma encontrada'},
            '404': {'description': 'Turma não encontrada'}
        }
    })
    def buscar_turma(id):
        turma = Turma.query.get(id)
        if not turma:
            return jsonify({'error': 'Turma não encontrada'}), 404

        return jsonify({
            'id': turma.id,
            'descricao': turma.descricao,
            'professor_id': turma.professor_id,
            'ativo': turma.ativo
        })

    @staticmethod
    @swag_from({
        'tags': ['Turmas'],
        'summary': 'Atualiza uma turma por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'descricao': {'type': 'string'},
                            'professor_id': {'type': 'integer'},
                            'ativo': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {'description': 'Turma atualizada com sucesso'},
            '404': {'description': 'Turma não encontrada'}
        }
    })
    def atualizar_turma(id):
        turma = Turma.query.get(id)
        if not turma:
            return jsonify({'error': 'Turma não encontrada'}), 404

        data = request.get_json()
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        turma.ativo = data.get('ativo', turma.ativo)

        db.session.commit()

        return jsonify({'message': 'Turma atualizada com sucesso'}), 200

    @staticmethod
    @swag_from({
        'tags': ['Turmas'],
        'summary': 'Remove uma turma por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '204': {'description': 'Turma removida com sucesso'},
            '404': {'description': 'Turma não encontrada'}
        }
    })
    def deletar_turma(id):
        turma = Turma.query.get(id)
        if not turma:
            return jsonify({'error': 'Turma não encontrada'}), 404

        db.session.delete(turma)
        db.session.commit()
        return '', 204
