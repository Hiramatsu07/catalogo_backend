from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something

class TaskModel(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    precio = db.Column(db.String)
    estado = db.Column(db.String)
    proveedor_id = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer)

    def __init__(self, id, descripcion, nombre,precio, estado,proveedor_id, catalogo_id):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.estado = estado
        self.proveedor_id = proveedor_id
        self.catalogo_id = catalogo_id

    def json(self, depth =0):
        json = {
            'id': self.id,
            'nombre' : self.nombre,
            'descripcion': self.descripcion,
            'precio' : self.precio,
            'estado': self.estado,
            'proveedor_id': self.proveedor_id,
            'catalogo_id' : self.catalogo_id
        }

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
        for no_pk_key in ['descripcion', 'estado', 'nombre', 'precio']:
            _assign_if_something(self, newdata, no_pk_key)

class CatModel(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String)

    def __init__(self, id, descripcion):
        self.id = id
        self.descripcion = descripcion

    def json(self, depth =0):
        json = {
            'id': self.id,
            'descripcion': self.descripcion,
        }

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
        for no_pk_key in ['description']:
            _assign_if_something(self, newdata, no_pk_key)

class ProvModel(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    direccion = db.Column(db.String)
    telefono = db.Column(db.String)

    def __init__(self, id, direccion, telefono):
        self.id = id
        self.direccion = direccion
        self.telefono = telefono

    def json(self, depth =0):
        json = {
            'id': self.id,
            'direccion': self.direccion,
            'telefono' : self.telefono
        }

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
        for no_pk_key in ['direccion, telefono']:
            _assign_if_something(self, newdata, no_pk_key)