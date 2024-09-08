from flask import Blueprint, request, jsonify
from app.model.escola import Escola
from app.db import db
from flasgger import swag_from
from sqlalchemy import and_

escola_routes = Blueprint('escola_routes', __name__)

@escola_routes.route('/escolas', methods=['POST'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Cria uma nova escola',
    'parameters': [
        {
            'name': 'escola',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'mensalidade': {'type': 'number'},
                    'quantidade_alunos': {'type': 'integer'},
                    'metodologia': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Escola criada com sucesso'
        }
    }
})
def create_escola():
    data = request.json
    new_escola = Escola(
        nome=data['nome'],
        telefone=data['telefone'],
        endereco=data['endereco'],
        mensalidade=data['mensalidade'],
        quantidade_alunos=data['quantidade_alunos'],
        metodologia=data['metodologia'],
        email=data['email']
    )
    db.session.add(new_escola)
    db.session.commit()
    return jsonify({"message": "Escola criada com sucesso"}), 201

@escola_routes.route('/escolas', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Lista todas as escolas',
    'responses': {
        200: {
            'description': 'Uma lista de escolas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_escolas():
    escolas = Escola.query.all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'endereco': e.endereco,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email
    } for e in escolas]
    return jsonify(result), 200

@escola_routes.route('/escolas/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Obter uma escola por ID',
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
            'description': 'Dados da escola',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nome': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'mensalidade': {'type': 'number'},
                    'quantidade_alunos': {'type': 'integer'},
                    'metodologia': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Escola não encontrada'
        }
    }
})
def get_escola(id):
    escola = Escola.query.get_or_404(id)
    result = {
        'id': escola.id,
        'nome': escola.nome,
        'telefone': escola.telefone,
        'endereco': escola.endereco,
        'mensalidade': escola.mensalidade,
        'quantidade_alunos': escola.quantidade_alunos,
        'metodologia': escola.metodologia,
        'email': escola.email
    }
    return jsonify(result), 200

@escola_routes.route('/escolas/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Atualiza uma escola existente',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'escola',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'endereco': {'type': 'string'},
                    'mensalidade': {'type': 'number'},
                    'quantidade_alunos': {'type': 'integer'},
                    'metodologia': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Escola atualizada com sucesso'
        },
        404: {
            'description': 'Escola não encontrada'
        }
    }
})
def update_escola(id):
    escola = Escola.query.get_or_404(id)
    data = request.json

    escola.nome = data.get('nome', escola.nome)
    escola.telefone = data.get('telefone', escola.telefone)
    escola.endereco = data.get('endereco', escola.endereco)
    escola.mensalidade = data.get('mensalidade', escola.mensalidade)
    escola.quantidade_alunos = data.get('quantidade_alunos', escola.quantidade_alunos)
    escola.metodologia = data.get('metodologia', escola.metodologia)
    escola.email = data.get('email', escola.email)

    db.session.commit()
    return jsonify({"message": "Escola atualizada com sucesso"}), 200

@escola_routes.route('/escolas/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Deleta uma escola existente',
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
            'description': 'Escola deletada com sucesso'
        },
        404: {
            'description': 'Escola não encontrada'
        }
    }
})
def delete_escola(id):
    escola = Escola.query.get_or_404(id)
    db.session.delete(escola)
    db.session.commit()
    return '', 204

# Rotas para filtros

@escola_routes.route('/escolas/filtro/metodologia', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Filtra escolas por metodologia',
    'parameters': [
        {
            'name': 'metodologia',
            'in': 'query',
            'required': True,
            'type': 'string'
        }
    ],
    'responses': {
        200: {
            'description': 'Escolas filtradas por metodologia',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def filtro_metodologia():
    metodologia = request.args.get('metodologia')
    escolas = Escola.query.filter(Escola.metodologia.ilike(f"%{metodologia}%")).all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'endereco': e.endereco,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email
    } for e in escolas]
    return jsonify(result), 200

@escola_routes.route('/escolas/filtro/preco', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Filtra escolas por preço (mensalidade)',
    'parameters': [
        {
            'name': 'min_preco',
            'in': 'query',
            'required': True,
            'type': 'number'
        },
        {
            'name': 'max_preco',
            'in': 'query',
            'required': True,
            'type': 'number'
        }
    ],
    'responses': {
        200: {
            'description': 'Escolas filtradas por faixa de preço',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def filtro_preco():
    min_preco = request.args.get('min_preco')
    max_preco = request.args.get('max_preco')
    escolas = Escola.query.filter(and_(Escola.mensalidade >= min_preco, Escola.mensalidade <= max_preco)).all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'endereco': e.endereco,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email
    } for e in escolas]
    return jsonify(result), 200

@escola_routes.route('/escolas/filtro/avaliacao', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Filtra escolas por avaliação (a ser implementado)',
    'parameters': [
        {
            'name': 'min_avaliacao',
            'in': 'query',
            'required': True,
            'type': 'number'
        }
    ],
    'responses': {
        200: {
            'description': 'Escolas filtradas por avaliação mínima (não implementado)',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def filtro_avaliacao():
    min_avaliacao = request.args.get('min_avaliacao')

    escolas = Escola.query.all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'endereco': e.endereco,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email
    } for e in escolas]
    return jsonify(result), 200

@escola_routes.route('/escolas/filtro/localizacao', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Filtra escolas por localização (a ser implementado)',
    'parameters': [
        {
            'name': 'latitude',
            'in': 'query',
            'required': True,
            'type': 'number'
        },
        {
            'name': 'longitude',
            'in': 'query',
            'required': True,
            'type': 'number'
        }
    ],
    'responses': {
        200: {
            'description': 'Escolas filtradas por proximidade (não implementado)',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'endereco': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def filtro_localizacao():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    # A implementação real deve utilizar a API de geocodificação do Google Maps para calcular a distância.
    # Este exemplo apenas retorna todas as escolas.
    escolas = Escola.query.all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'endereco': e.endereco,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email
    } for e in escolas]
    return jsonify(result), 200
