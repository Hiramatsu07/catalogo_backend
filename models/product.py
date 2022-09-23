from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something
from models.category import CatModel
from models.provider import ProvModel

class ProductModel(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    precio = db.Column(db.String)
    estado = db.Column(db.String)
    proveedor_id = db.Column(db.Integer, db.ForeignKey(ProvModel.id))
    categoria_id = db.Column(db.Integer, db.ForeignKey(CatModel.id))

    _proveedor = db.relationship('ProvModel', 
        uselist=False, 
        primaryjoin='ProvModel.id == ProductModel.proveedor_id', 
        foreign_keys='ProductModel.proveedor_id')

    _categoria = db.relationship('CatModel', 
        uselist=False,
        primaryjoin='CatModel.id == ProductModel.categoria_id', 
        foreign_keys='ProductModel.categoria_id')

    def __init__(self, id, descripcion, estado, nombre, precio, proveedor_id, categoria_id):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio
        self.nombre = nombre
        self.estado = estado
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id

    def json(self, depth =0):
        json = {
            'id': self.id,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'nombre': self.nombre,
            'precio': self.precio,
            'proveedor_id': self.proveedor_id,
            'categoria_id': self.categoria_id
        }
        if depth > 0:
            if self._proveedor:
                json['_provider'] = self._proveedor.json(depth)
            
            if self._categoria:
                json['_categoria'] = self._categoria.json(depth)

        return json


    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def from_reqparse(self, newdata: Namespace):
        for no_pk_key in ['descripcion', 'estado', 'nombre', 'precio', 'proveedor_id', 'categoria_id']:
            _assign_if_something(self, newdata, no_pk_key)