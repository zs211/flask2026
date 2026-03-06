from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_mail import Mail

class Base(DeclarativeBase):
    meta = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(column_0_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referrer_id)s',
        'pk': 'pk_%(table_name)s'
    })

db = SQLAlchemy(model_class=Base)

migrate = Migrate()
mail = Mail()