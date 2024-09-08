#criei o arquivo db separado pois tive problema com ele de importação circular, removi onde ele era chamdo e deixei so no arquivo separdo visto que uso o db em   "packs" diferentes
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
