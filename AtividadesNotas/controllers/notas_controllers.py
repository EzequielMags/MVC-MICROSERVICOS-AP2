from flask import request, jsonify
from models import db
from models.notas import Notas
from flasgger import swag_from

class NotasController:

    @staticmethod
    @swag_from({
        'tags': ['Notas'],
        'summary': 'Listar todas as notas',
        'responses': {
            '200': {
                'description': 'Lista de notas retornada com sucesso',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'nota': 8.5,
                                'aluno_id': 3,
                                'atividade_id': 2
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_notas():
        notas = Notas.query.all()
        notas_list = [nota.to_dict() for nota in notas]
        return jsonify(notas_list), 200

    @staticmethod
    @swag_from({
        'tags': ['Notas'],
        'summary': 'Buscar nota por ID',
        'parameters': [
            {
                'name': 'nota_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da nota a ser buscada'
            }
        ],
        'responses': {
            '200': {'description': 'Nota encontrada'},
            '404': {'description': 'Nota não encontrada'}
        }
    })
    def buscar_nota_por_id(nota_id):
        nota = Notas.query.get(nota_id)
        if nota:
            return jsonify(nota.to_dict()), 200
        else:
            return jsonify({'message': 'Nota não encontrada'}), 404

    @staticmethod
    @swag_from({
        'tags': ['Notas'],
        'summary': 'Criar uma nova nota',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'nota': {'type': 'number', 'format': 'float'},
                            'aluno_id': {'type': 'integer'},
                            'atividade_id': {'type': 'integer'}
                        },
                        'required': ['nota', 'aluno_id', 'atividade_id']
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Nota criada com sucesso',
                'content': {
                    'application/json': {
                        'example': {
                            'id': 1,
                            'nota': 9.0,
                            'aluno_id': 3,
                            'atividade_id': 2
                        }
                    }
                }
            }
        }
    })
    def criar_nota():
        data = request.get_json()
        nova_nota = Notas(
            nota=data['nota'],
            aluno_id=data['aluno_id'],
            atividade_id=data['atividade_id']
        )
        db.session.add(nova_nota)
        db.session.commit()
        return jsonify(nova_nota.to_dict()), 201

    @staticmethod
    @swag_from({
        'tags': ['Notas'],
        'summary': 'Atualizar uma nota existente',
        'parameters': [
            {
                'name': 'nota_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da nota a ser atualizada'
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'nota': {'type': 'number', 'format': 'float'},
                            'aluno_id': {'type': 'integer'},
                            'atividade_id': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {'description': 'Nota atualizada com sucesso'},
            '404': {'description': 'Nota não encontrada'}
        }
    })
    def atualizar_nota(nota_id):
        data = request.get_json()
        nota = Notas.query.get(nota_id)
        if not nota:
            return jsonify({'message': 'Nota não encontrada'}), 404

        nota.nota = data.get('nota', nota.nota)
        nota.aluno_id = data.get('aluno_id', nota.aluno_id)
        nota.atividade_id = data.get('atividade_id', nota.atividade_id)

        db.session.commit()
        return jsonify(nota.to_dict()), 200

    @staticmethod
    @swag_from({
        'tags': ['Notas'],
        'summary': 'Deletar uma nota',
        'parameters': [
            {
                'name': 'nota_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da nota a ser deletada'
            }
        ],
        'responses': {
            '200': {'description': 'Nota deletada com sucesso'},
            '404': {'description': 'Nota não encontrada'}
        }
    })
    def deletar_nota(nota_id):
        nota = Notas.query.get(nota_id)
        if not nota:
            return jsonify({'message': 'Nota não encontrada'}), 404

        db.session.delete(nota)
        db.session.commit()
        return jsonify({'message': 'Nota deletada com sucesso'}), 200
