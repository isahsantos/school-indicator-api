from flask import Blueprint, request, jsonify
from app.model.pais import Pais
from app.schema.pais_schema import PaisSchema
from app.db import db
from flasgger import swag_from

pais_routes = Blueprint('pais_routes', __name__)
pais_schema = PaisSchema()
paises_schema = PaisSchema(many=True)

@pais_routes.route('/pais', methods=['POST'])
@swag_from({
    'tags': ['Pais'],
    'description': 'Cadastra um novo pai ou responsável',
    'parameters': [
        {
            'name': 'pai',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_completo': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'idade_crianca': {'type': 'integer'},
                    'necessidades_especiais': {'type': 'boolean'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Pai cadastrado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nome_completo': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'idade_crianca': {'type': 'integer'},
                    'necessidades_especiais': {'type': 'boolean'},
                    'email': {'type': 'string'}
                }
            }
        }
    }
})
def create_pais():
    data = request.json
    new_pais = Pais(
        nome_completo=data['nome_completo'],
        telefone=data['telefone'],
        endereco=data['endereco'],
        idade_crianca=data['idade_crianca'],
        necessidades_especiais=data['necessidades_especiais'],
        email=data['email']
    )
    db.session.add(new_pais)
    db.session.commit()
    return pais_schema.jsonify(new_pais), 201

@pais_routes.route('/pais', methods=['GET'])
@swag_from({
    'tags': ['Pais'],
    'description': 'Lista todos os pais ou responsáveis',
    'responses': {
        200: {
            'description': 'Uma lista de pais ou responsáveis',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome_completo': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'idade_crianca': {'type': 'integer'},
                        'necessidades_especiais': {'type': 'boolean'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_paises():
    paises = Pais.query.all()
    return paises_schema.jsonify(paises), 200

@pais_routes.route('/pais/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Pais'],
    'description': 'Obtém os detalhes de um pai ou responsável específico',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes do pai ou responsável',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nome_completo': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'idade_crianca': {'type': 'integer'},
                    'necessidades_especiais': {'type': 'boolean'},
                    'email': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Pai ou responsável não encontrado'
        }
    }
})
def get_pais(id):
    pais = Pais.query.get_or_404(id)
    return pais_schema.jsonify(pais), 200

@pais_routes.route('/pais/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Pais'],
    'description': 'Atualiza os detalhes de um pai ou responsável específico',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'pai',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_completo': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'idade_crianca': {'type': 'integer'},
                    'necessidades_especiais': {'type': 'boolean'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Pai atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nome_completo': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'idade_crianca': {'type': 'integer'},
                    'necessidades_especiais': {'type': 'boolean'},
                    'email': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Pai ou responsável não encontrado'
        }
    }
})
def update_pais(id):
    pais = Pais.query.get_or_404(id)
    data = request.json

    pais.nome_completo = data.get('nome_completo', pais.nome_completo)
    pais.telefone = data.get('telefone', pais.telefone)
    pais.endereco = data.get('endereco', pais.endereco)
    pais.idade_crianca = data.get('idade_crianca', pais.idade_crianca)
    pais.necessidades_especiais = data.get('necessidades_especiais', pais.necessidades_especiais)
    pais.email = data.get('email', pais.email)

    db.session.commit()
    return pais_schema.jsonify(pais), 200

@pais_routes.route('/pais/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Pais'],
    'description': 'Deleta um pai ou responsável específico',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        204: {
            'description': 'Pai ou responsável deletado com sucesso'
        },
        404: {
            'description': 'Pai ou responsável não encontrado'
        }
    }
})
def delete_pais(id):
    pais = Pais.query.get_or_404(id)
    db.session.delete(pais)
    db.session.commit()
    return '', 204
