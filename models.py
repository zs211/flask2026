from typing import List
from werkzeug.security import generate_password_hash,check_password_hash
from exts import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey,Text
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id :Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    username :Mapped[str] = mapped_column(db.String(80))
    _password :Mapped[str] =  mapped_column(db.String(200))
    email :Mapped[str] = mapped_column(db.String(80),unique=True)
    vegetables :Mapped["Vegetable"] = relationship("Vegetable",back_populates='publisher')

    def __init__(self,*args,**kwargs):
        password = kwargs.get('password')
        if password:
            kwargs.pop('password')
        super().__init__(*args,**kwargs)
        self.password = password

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)
    def check_password_hash(self,raw_password):
        return check_password_hash(self._password,raw_password)

class VegetableCategory(db.Model):
    __tablename__ = 'vegetable_category'
    id :Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name :Mapped[str] = mapped_column(db.String(80))
    vegetables :Mapped[List["Vegetable"]] = relationship("Vegetable",back_populates='category')
class Vegetable(db.Model):
    __tablename__ = 'vegetable'

    id :Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name :Mapped[str] = mapped_column(db.String(80))
    content :Mapped[str] = mapped_column(Text)
    price :Mapped[float] = mapped_column(db.Float)
    picture :Mapped[str] = mapped_column(db.String(80))
    mobile :Mapped[str] = mapped_column(db.String(80))
    place :Mapped[str] = mapped_column(db.String(80))
    provider :Mapped[str] = mapped_column(db.String(80))
    pub_date :Mapped[str] = mapped_column(db.DateTime,default = datetime.now())
    category_id :Mapped[int] = mapped_column(db.Integer,ForeignKey('vegetable_category.id'))
    category :Mapped[VegetableCategory] = relationship(VegetableCategory,back_populates='vegetables')

    publish_id :Mapped[int] = mapped_column(db.Integer,ForeignKey(User.id))
    publisher:Mapped[User] = relationship(User,back_populates='vegetables')

class EmailCode(db.Model):
    __tablename__ = 'email_code'
    id :Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    code :Mapped[str] = mapped_column(db.String(80))
    email :Mapped[str] = mapped_column(db.String(80))
    created_time :Mapped[datetime] = mapped_column(db.DateTime,default = datetime.now())