from app.db import db

class Avaliacao(db.Model):  
    __tablename__ = 'avaliacao'
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    nome_avaliador = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.String(200))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

class Escola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)  
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    mensalidade = db.Column(db.Float, nullable=False)
    quantidade_alunos = db.Column(db.Integer, nullable=False)
    metodologia = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    avaliacao = db.Column(db.Float)
