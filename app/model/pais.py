from app.db import db

class Pais(db.Model):
    __tablename__ = 'pais'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    idade_crianca = db.Column(db.Integer, nullable=False)
    necessidades_especiais = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(100), nullable=False)
