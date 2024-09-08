from app.db import ma
from app.model.pais import Pais

class PaisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True
