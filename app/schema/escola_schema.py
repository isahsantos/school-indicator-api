from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.model.escola import Escola, Avaliacao

class AvaliacaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Avaliacao

class EscolaSchema(SQLAlchemyAutoSchema):
    avaliacoes = fields.Nested(AvaliacaoSchema, many=True)

    class Meta:
        model = Escola
