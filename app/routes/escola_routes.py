from flask import Blueprint, request, jsonify
from app.model.escola import Escola
from app.db import db
from flasgger import swag_from
from sqlalchemy import and_
import requests

escola_routes = Blueprint('escola_routes', __name__)

def buscar_endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
                    'cep': {'type': 'string'},
                    'numero': {'type': 'string'},  
                    'mensalidade': {'type': 'number'},
                    'quantidade_alunos': {'type': 'integer'},
                    'metodologia': {'type': 'string'},
                    'email': {'type': 'string'}
                },
                'example': {
                    'nome': 'Escola Exemplo',
                    'telefone': '(11) 1234-5678',
                    'cep': '01000-000',
                    'numero': '123',  
                    'mensalidade': 1500.00,
                    'quantidade_alunos': 250,
                    'metodologia': 'Construtivista',
                    'email': 'contato@escolaexemplo.com.br'
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Escola criada com sucesso'
        },
        400: {
            'description': 'Erro ao criar a escola'
        }
    }
})
def create_escola():
    data = request.json

    cep_info = buscar_endereco_por_cep(data['cep'])
    if not cep_info or 'erro' in cep_info:
        return jsonify({"error": "CEP inválido"}), 400

    new_escola = Escola(
        nome=data['nome'],
        telefone=data['telefone'],
        rua=cep_info['logradouro'],
        numero=data['numero'],  
        bairro=cep_info['bairro'],
        cidade=cep_info['localidade'],
        estado=cep_info['uf'],
        cep=data['cep'],
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
                        'rua': {'type': 'string'},
                        'numero': {'type': 'string'},  
                        'bairro': {'type': 'string'},
                        'cidade': {'type': 'string'},
                        'estado': {'type': 'string'},
                        'cep': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avaliacao': {'type': 'number'}
                    }
                },
                'example': [
                    {
                        'id': 1,
                        'nome': 'Escola Exemplo',
                        'telefone': '(11) 1234-5678',
                        'rua': 'Rua das Flores',
                        'numero': '123', 
                        'bairro': 'Centro',
                        'cidade': 'São Paulo',
                        'estado': 'SP',
                        'cep': '01000-000',
                        'mensalidade': 1500.00,
                        'quantidade_alunos': 250,
                        'metodologia': 'Construtivista',
                        'email': 'contato@escolaexemplo.com.br',
                        'avaliacao': 4.5
                    }
                ]
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
        'rua': e.rua,
        'numero': e.numero, 
        'bairro': e.bairro,
        'cidade': e.cidade,
        'estado': e.estado,
        'cep': e.cep,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email,
        'avaliacao': e.avaliacao
    } for e in escolas]
    return jsonify(result), 200

@escola_routes.route('/escolas/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Obtém os detalhes de uma escola por ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID da escola'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes da escola',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nome': {'type': 'string'},
                    'telefone': {'type': 'string'},
                    'rua': {'type': 'string'},
                    'numero': {'type': 'string'}, 
                    'bairro': {'type': 'string'},
                    'cidade': {'type': 'string'},
                    'estado': {'type': 'string'},
                    'cep': {'type': 'string'},
                    'mensalidade': {'type': 'number'},
                    'quantidade_alunos': {'type': 'integer'},
                    'metodologia': {'type': 'string'},
                    'email': {'type': 'string'},
                    'avaliacao': {'type': 'number'}
                },
                'example': {
                    'id': 1,
                    'nome': 'Escola Exemplo',
                    'telefone': '(11) 1234-5678',
                    'rua': 'Rua das Flores',
                    'numero': '123', 
                    'bairro': 'Centro',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'cep': '01000-000',
                    'mensalidade': 1500.00,
                    'quantidade_alunos': 250,
                    'metodologia': 'Construtivista',
                    'email': 'contato@escolaexemplo.com.br',
                    'avaliacao': 4.5
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
        'rua': escola.rua,
        'numero': escola.numero, 
        'bairro': escola.bairro,
        'cidade': escola.cidade,
        'estado': escola.estado,
        'cep': escola.cep,
        'mensalidade': escola.mensalidade,
        'quantidade_alunos': escola.quantidade_alunos,
        'metodologia': escola.metodologia,
        'email': escola.email,
        'avaliacao': escola.avaliacao
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
            'type': 'integer',
            'description': 'ID da escola a ser atualizada'
        },
        {
            'name': 'escola',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string', 'description': 'Nome da escola'},
                    'telefone': {'type': 'string', 'description': 'Telefone da escola'},
                    'rua': {'type': 'string', 'description': 'Rua da escola'},
                    'numero': {'type': 'string', 'description': 'Número do endereço'}, 
                    'bairro': {'type': 'string', 'description': 'Bairro da escola'},
                    'cidade': {'type': 'string', 'description': 'Cidade da escola'},
                    'estado': {'type': 'string', 'description': 'Estado da escola (UF)'},
                    'cep': {'type': 'string', 'description': 'CEP da escola'},
                    'mensalidade': {'type': 'number', 'description': 'Mensalidade da escola'},
                    'quantidade_alunos': {'type': 'integer', 'description': 'Quantidade de alunos matriculados'},
                    'metodologia': {'type': 'string', 'description': 'Metodologia de ensino da escola'},
                    'email': {'type': 'string', 'description': 'Email de contato da escola'},
                    'avaliacao': {'type': 'number', 'description': 'Avaliação média da escola'}
                },
                'example': {
                    'nome': 'Escola Exemplo',
                    'telefone': '(11) 1234-5678',
                    'rua': 'Rua das Flores',
                    'numero': '123',  
                    'bairro': 'Centro',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'cep': '01000-000',
                    'mensalidade': 1500.00,
                    'quantidade_alunos': 250,
                    'metodologia': 'Construtivista',
                    'email': 'contato@escolaexemplo.com.br',
                    'avaliacao': 4.5
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

    if 'cep' in data:
        cep_info = buscar_endereco_por_cep(data['cep'])
        if not cep_info or 'erro' in cep_info:
            return jsonify({"error": "CEP inválido"}), 400

        escola.rua = cep_info.get('logradouro', escola.rua)
        escola.bairro = cep_info.get('bairro', escola.bairro)
        escola.cidade = cep_info.get('localidade', escola.cidade)
        escola.estado = cep_info.get('uf', escola.estado)
        escola.cep = data['cep']

    escola.nome = data.get('nome', escola.nome)
    escola.telefone = data.get('telefone', escola.telefone)
    escola.numero = data.get('numero', escola.numero)  
    escola.mensalidade = data.get('mensalidade', escola.mensalidade)
    escola.quantidade_alunos = data.get('quantidade_alunos', escola.quantidade_alunos)
    escola.metodologia = data.get('metodologia', escola.metodologia)
    escola.email = data.get('email', escola.email)
    escola.avaliacao = data.get('avaliacao', escola.avaliacao)

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
            'type': 'integer',
            'description': 'ID da escola a ser deletada'
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

@escola_routes.route('/escolas/filtro/metodologia', methods=['GET'])
@swag_from({
    'tags': ['Escolas'],
    'description': 'Filtra escolas por metodologia',
    'parameters': [
        {
            'name': 'metodologia',
            'in': 'query',
            'required': True,
            'type': 'string',
            'description': 'Metodologia de ensino da escola'
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
                        'rua': {'type': 'string'},
                        'numero': {'type': 'string'},  
                        'bairro': {'type': 'string'},
                        'cidade': {'type': 'string'},
                        'estado': {'type': 'string'},
                        'cep': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avaliacao': {'type': 'number'}
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
        'rua': e.rua,
        'numero': e.numero,  
        'bairro': e.bairro,
        'cidade': e.cidade,
        'estado': e.estado,
        'cep': e.cep,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email,
        'avaliacao': e.avaliacao
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
            'type': 'number',
            'description': 'Preço mínimo da mensalidade'
        },
        {
            'name': 'max_preco',
            'in': 'query',
            'required': True,
            'type': 'number',
            'description': 'Preço máximo da mensalidade'
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
                        'rua': {'type': 'string'},
                        'numero': {'type': 'string'},
                        'bairro': {'type': 'string'},
                        'cidade': {'type': 'string'},
                        'estado': {'type': 'string'},
                        'cep': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avaliacao': {'type': 'number'}
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
        'rua': e.rua,
        'numero': e.numero, 
        'bairro': e.bairro,
        'cidade': e.cidade,
        'estado': e.estado,
        'cep': e.cep,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email,
        'avaliacao': e.avaliacao
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
            'type': 'number',
            'description': 'Avaliação mínima'
        }
    ],
    'responses': {
        200: {
            'description': 'Escolas filtradas por avaliação mínima',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'rua': {'type': 'string'},
                        'numero': {'type': 'string'}, 
                        'bairro': {'type': 'string'},
                        'cidade': {'type': 'string'},
                        'estado': {'type': 'string'},
                        'cep': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avaliacao': {'type': 'number'}
                    }
                }
            }
        }
    }
})
def filtro_avaliacao():
    min_avaliacao = request.args.get('min_avaliacao')

    escolas = Escola.query.filter(Escola.avaliacao >= min_avaliacao).all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'rua': e.rua,
        'numero': e.numero,  
        'bairro': e.bairro,
        'cidade': e.cidade,
        'estado': e.estado,
        'cep': e.cep,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email,
        'avaliacao': e.avaliacao
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
            'type': 'number',
            'description': 'Latitude do ponto de referência'
        },
        {
            'name': 'longitude',
            'in': 'query',
            'required': True,
            'type': 'number',
            'description': 'Longitude do ponto de referência'
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
                        'rua': {'type': 'string'},
                        'numero': {'type': 'string'},  
                        'bairro': {'type': 'string'},
                        'cidade': {'type': 'string'},
                        'estado': {'type': 'string'},
                        'cep': {'type': 'string'},
                        'mensalidade': {'type': 'number'},
                        'quantidade_alunos': {'type': 'integer'},
                        'metodologia': {'type': 'string'},
                        'email': {'type': 'string'},
                        'avaliacao': {'type': 'number'}
                    }
                }
            }
        }
    }
})
def filtro_localizacao():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    escolas = Escola.query.all()
    result = [{
        'id': e.id,
        'nome': e.nome,
        'telefone': e.telefone,
        'rua': e.rua,
        'numero': e.numero,  
        'bairro': e.bairro,
        'cidade': e.cidade,
        'estado': e.estado,
        'cep': e.cep,
        'mensalidade': e.mensalidade,
        'quantidade_alunos': e.quantidade_alunos,
        'metodologia': e.metodologia,
        'email': e.email,
        'avaliacao': e.avaliacao
    } for e in escolas]
    return jsonify(result), 200
