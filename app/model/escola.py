from app.db import db

class Avaliacao(db.Model):  
    __tablename__ = 'avaliacao'
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    nome_avaliador = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.String(200))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

class Escola(db.Model):
    __tablename__ = 'escola'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    mensalidade = db.Column(db.Float, nullable=False)
    quantidade_alunos = db.Column(db.Integer, nullable=False)
    metodologia = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    avaliacoes = db.relationship('Avaliacao', backref='escola', lazy=True)  
