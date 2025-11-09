from flask import request, jsonify
from models.aluno import Aluno
from models import db
from flasgger import swag_from
from datetime import datetime
import requests

def get_turma(turma_id: int):
    try:
        response = requests.get(f"http://127.0.0.1:5000/turmas/{turma_id}")
        if response.status_code == 200:
            return response.json()  # retorna os dados da turma
        return None  # turma não encontrada
    except requests.RequestException as e:
        print(f"Erro ao buscar turma: {e}")
        return None

class AlunoController:

    @staticmethod
    @swag_from({
        'tags': ['Alunos'],
        'summary': 'Lista todos os alunos',
        'responses': {
            '200': {
                'description': 'Lista de alunos',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'nome': 'Maria',
                                'idade': 16,
                                'turma_id': 2,
                                'data_nascimento': '2009-03-10'
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_alunos():
        alunos = Aluno.query.all()
        return jsonify([
            {
                'id': a.id,
                'nome': a.nome,
                'idade': a.idade,
                'turma_id': a.turma_id,
                'data_nascimento': a.data_nascimento.isoformat() if a.data_nascimento else None
            } for a in alunos
        ]), 200

    @staticmethod
    @swag_from({
        'tags': ['Alunos'],
        'summary': 'Cria um novo aluno',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'nome': {'type': 'string'},
                            'idade': {'type': 'integer'},
                            'turma_id': {'type': 'integer'},
                            'data_nascimento': {'type': 'string', 'format': 'date'}
                        },
                        'required': ['nome', 'idade', 'turma_id']
                    },
                    'example': {
                        'nome': 'Maria',
                        'idade': 16,
                        'turma_id': 2,
                        'data_nascimento': '2009-03-10'
                    }
                }
            }
        },
        'responses': {
            '201': {'description': 'Aluno criado com sucesso'},
            '400': {'description': 'Dados inválidos'}
        }
    })
    def criar_aluno():
        data = request.get_json(silent=True) or {}

        nome = data.get('nome')
        idade = data.get('idade')
        turma_id = data.get('turma_id')
        data_nascimento = data.get('data_nascimento')

        turma = get_turma(data["turma_id"])

        if not turma:
            return jsonify({'message': 'turma não encontrada'}), 400

        if not nome or not idade or not turma_id:
            return jsonify({'error': 'nome, idade e turma_id são obrigatórios'}), 400

        try:
            nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date() if data_nascimento else None
        except ValueError:
            return jsonify({'error': 'data_nascimento deve estar no formato YYYY-MM-DD'}), 400

        aluno = Aluno(
            nome=nome,
            idade=idade,
            turma_id=turma_id,
            data_nascimento=nascimento
        )
        db.session.add(aluno)
        db.session.commit()

        return jsonify({
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'turma_id': aluno.turma_id,
            'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None
        }), 201

    @staticmethod
    @swag_from({
        'tags': ['Alunos'],
        'summary': 'Busca um aluno por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '200': {'description': 'Aluno encontrado'},
            '404': {'description': 'Aluno não encontrado'}
        }
    })
    def buscar_aluno(id):
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404

        return jsonify({
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'turma_id': aluno.turma_id,
            'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None
        }), 200

    @staticmethod
    @swag_from({
        'tags': ['Alunos'],
        'summary': 'Atualiza um aluno por ID',
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
                            'turma_id': {'type': 'integer'},
                            'data_nascimento': {'type': 'string'}
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {'description': 'Aluno atualizado com sucesso'},
            '404': {'description': 'Aluno não encontrado'}
        }
    })
    def atualizar_aluno(id):
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404

        data = request.get_json()

        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)

        nascimento = data.get('data_nascimento')
        if nascimento:
            try:
                aluno.data_nascimento = datetime.strptime(nascimento, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'data_nascimento inválida'}), 400

        db.session.commit()

        return jsonify({'message': 'Aluno atualizado com sucesso'}), 200

    @staticmethod
    @swag_from({
        'tags': ['Alunos'],
        'summary': 'Remove um aluno por ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '204': {'description': 'Aluno removido com sucesso'},
            '404': {'description': 'Aluno não encontrado'}
        }
    })
    def deletar_aluno(id):
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404

        db.session.delete(aluno)
        db.session.commit()
        return '', 204
