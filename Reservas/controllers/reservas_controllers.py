from flask import request, jsonify
from models import db
from models.reservas import Reservas
from flasgger import swag_from
from datetime import datetime
import requests

def get_turma(turma_id: int):
    try:
        response = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
        if response.status_code == 200:
            return response.json()  # retorna os dados da turma
        return None  # turma não encontrada
    except requests.RequestException as e:
        print(f"Erro ao buscar turma: {e}")
        return None


class ReservasController:

    @staticmethod
    @swag_from({
        'tags': ['Reservas'],
        'summary': 'Listar todas as reservas',
        'responses': {
            '200': {
                'description': 'Lista de reservas retornada com sucesso',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'id': 1,
                                'num_sala': 204,
                                'lab': True,
                                'data': '2025-10-31',
                                'turma_id': 3
                            }
                        ]
                    }
                }
            }
        }
    })
    def listar_reservas():
        reservas = Reservas.query.order_by(Reservas.id.asc()).all()
        reservas_list = [reserva.to_dict() for reserva in reservas]
        return jsonify(reservas_list), 200

    @staticmethod
    @swag_from({
        'tags': ['Reservas'],
        'summary': 'Buscar reserva por ID',
        'parameters': [
            {
                'name': 'reserva_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da reserva a ser buscada'
            }
        ],
        'responses': {
            '200': {'description': 'Reserva encontrada'},
            '404': {'description': 'Reserva não encontrada'}
        }
    })
    def buscar_reserva_por_id(reserva_id):
        reserva = Reservas.query.get(reserva_id)
        if reserva:
            return jsonify(reserva.to_dict()), 200
        return jsonify({'message': 'Reserva não encontrada'}), 404

    @staticmethod
    @swag_from({
        'tags': ['Reservas'],
        'summary': 'Criar uma nova reserva',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'num_sala': {'type': 'integer'},
                            'lab': {'type': 'boolean'},
                            'data': {'type': 'string', 'format': 'date'},
                            'turma_id': {'type': 'integer'}
                        },
                        'required': ['num_sala', 'lab', 'data', 'turma_id']
                    }
                }
            }
        },
        'responses': {
            '201': {'description': 'Reserva criada com sucesso'}
        }
    })
    def criar_reserva():
        data = request.get_json()

        turma = get_turma(data["turma_id"])

        if not turma:
            return jsonify({'message': 'turma não encontrada'}), 400
            
        data_str = data.get('data')
        data_convertida = datetime.strptime(data_str, '%Y-%m-%d').date()
        nova_reserva = Reservas(
            id=data['id'],
            num_sala=data['num_sala'],
            lab=data['lab'],
            data=data_convertida,
            turma_id=data['turma_id']
        )
        db.session.add(nova_reserva)
        db.session.commit()
        return jsonify(nova_reserva.to_dict()), 201

    @staticmethod
    @swag_from({
        'tags': ['Reservas'],
        'summary': 'Atualizar uma reserva existente',
        'parameters': [
            {

                'name': 'reserva_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da reserva a ser atualizada'
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'num_sala': {'type': 'integer'},
                            'lab': {'type': 'boolean'},
                            'data': {'type': 'string', 'format': 'date'},
                            'turma_id': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {'description': 'Reserva atualizada com sucesso'},
            '404': {'description': 'Reserva não encontrada'}
        }
    })
    def atualizar_reserva(reserva_id):
        data = request.get_json()
        reserva = Reservas.query.get(reserva_id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 40

        reserva.id = data.get('id', reserva.id)
        reserva.num_sala = data.get('num_sala', reserva.num_sala)
        reserva.lab = data.get('lab', reserva.lab)
        reserva.data = data.get('data', reserva.data)
        reserva.turma_id = data.get('turma_id', reserva.turma_id)

        db.session.commit()
        return jsonify(reserva.to_dict()), 200

    @swag_from({
        'tags': ['Reservas'],
        'summary': 'Deletar uma reserva',
        'parameters': [
            {
                'name': 'reserva_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID da reserva a ser deletada'
            }
        ],
        'responses': {
            '200': {'description': 'Reserva deletada com sucesso'},
            '404': {'description': 'Reserva não encontrada'}
        }
    })
    def deletar_reserva(reserva_id):
        reserva = Reservas.query.get(reserva_id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 404
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({'message': 'Reserva deletada com sucesso'}), 200