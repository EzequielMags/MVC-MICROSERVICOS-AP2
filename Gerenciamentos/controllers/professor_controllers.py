from flask import request, jsonify
from models.professor import Professor
from models import db
from flasgger import swag_from

class ProfessorController:
    
    @staticmethod
    @swag_from({
        'tags': ['Professores'],
        'summary': 'Lista todos os professores',
        'responses': {
            '200': {
                'description': 'Lista de professores',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'nome': 'João da Silva',
                                'idade': 45,
                                'materia': 'Matemática',
                                'observacoes': 'Mestre em Educação'
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_professores():
        professores = Professor.query.all()
        return jsonify([p.to_dict() for p in professores]), 200

    @staticmethod
    @swag_from({
        'tags': ['Professores'],
        'summary': 'Cria um novo professor',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'nome': {'type': 'string'},
                            'idade': {'type': 'integer'},
                            'materia': {'type': 'string'},
                            'observacoes': {'type': 'string'}
                        },
                        'required': ['nome', 'idade', 'materia']
                    },
                    'example': {
                        'nome': 'João da Silva',
                        'idade': 45,
                        'materia': 'Matemática',
                        'observacoes': 'Mestre em Educação'
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Professor criado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            }
        }
    })
    def criar_professor():
        data = request.get_json(silent=True) or {}

        nome = data.get('nome')
        idade = data.get('idade')
        materia = data.get('materia')
        observacoes = data.get('observacoes', '')

        if not nome or not idade or not materia:
            return jsonify({'error': 'nome, idade e materia são obrigatórios'}), 400

        professor = Professor(
            nome=nome,
            idade=idade,
            materia=materia,
            observacoes=observacoes
        )
        db.session.add(professor)
        db.session.commit()

        return jsonify(professor.to_dict()), 201

    @staticmethod
    @swag_from({
        'tags': ['Professores'],
        'summary': 'Busca um professor por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '200': {'description': 'Professor encontrado'},
            '404': {'description': 'Professor não encontrado'}
        }
    })
    def buscar_professor(id):
        professor = Professor.query.get(id)
        if not professor:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        return jsonify({
            'id': professor.id,
            'nome': professor.nome,
            'idade': professor.idade,
            'materia': professor.materia,
            'observacoes': professor.observacoes
        })

    @staticmethod
    @swag_from({
        'tags': ['Professores'],
        'summary': 'Atualiza um professor por ID',
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
                            'nome': {'type': 'string'},
                            'idade': {'type': 'integer'},
                            'materia': {'type': 'string'},
                            'observacoes': {'type': 'string'}
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {'description': 'Professor atualizado com sucesso'},
            '404': {'description': 'Professor não encontrado'}
        }
    })
    def atualizar_professor(id):
        professor = Professor.query.get(id)
        if not professor:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        data = request.get_json()
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)

        db.session.commit()

        return jsonify({'message': 'Professor atualizado com sucesso'})

    @staticmethod
    @swag_from({
        'tags': ['Professores'],
        'summary': 'Remove um professor por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '204': {'description': 'Professor removido com sucesso'},
            '404': {'description': 'Professor não encontrado'}
        }
    })
    def deletar_professor(id):
        professor = Professor.query.get(id)
        if not professor:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        db.session.delete(professor)
        db.session.commit()
        return '', 204
