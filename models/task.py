from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something

class TaskModel(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    descrip = db.Column(db.String)
    status = db.Column(db.String)

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

    