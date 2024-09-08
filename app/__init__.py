import os
from flask import Flask
from app.db import db, ma
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Verifica se o diretorio instance para db esteja criado, pois tive problemas por esse diretório não esta criado. 
    
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{instance_path}/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    swagger_template = {
        "info": {
            "title": "API para sugestão de escolas",
            "description": "API para busca de escolas, o projeto visa facilitar os pais a encontrar escolas para seus filhos, projeto realizado para conclusção de sprint  da pós graduação de desenvolvimento full stack da PUC RIO digital.",
            "version": "1.0.0",
            "contact": {
                "name": "Maria Isabela dos Santos Silva",
                "email": "isa2014mgspn@gmail.com",
                "linkedin": "https://www.linkedin.com/in/isabela-santos-si/",
                
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },
        },
        "host": "localhost:5000", 
        "basePath": "/",  # Base path para todas as rotas
        "schemes": [
            "http",
            "https"
        ],
        "tags": [
            {
                "name": "Escolas",
                "description": "Operações relacionadas a escolas"
            },
            {
                "name": "Pais",
                "description": "Operações relacionadas a pais"
            },
        ],
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  
                "model_filter": lambda tag: True,  # 
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    Swagger(app, template=swagger_template, config=swagger_config)

    from app.routes.escola_routes import escola_routes
    from app.routes.pais_routes import pais_routes
    app.register_blueprint(escola_routes, url_prefix='/api')
    app.register_blueprint(pais_routes, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
