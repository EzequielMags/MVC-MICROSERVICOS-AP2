from flask import request, jsonify
from models import db
from models.reservas import Reservas
from flasgger import swag_from

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
        nova_reserva = Reservas(
            num_sala=data['num_sala'],
            lab=data['lab'],
            data=data['data'],
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