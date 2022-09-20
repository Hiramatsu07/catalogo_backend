from tkinter import E
from models.task import CatModel, TaskModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request

from utils import paginated_results, _assign_if_something, restrict

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('descripcion', type = str)
    parser.add_argument('estado', type = str)
    parser.add_argument('nombre', type = str)
    parser.add_argument('proveedor_id', type = int)
    parser.add_argument('categoria_id', type = int)

    @swag_from('../swagger/product/get_product.yaml')
    def getProduct(self):
        tarea = TaskModel.find_by_id()
        if tarea:
            return tarea.json()
        return {'message': 'Nein'}, 404        

    @swag_from('../swagger/product/put_product.yaml')
    def put(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            newdata = Task.parser.parse_args()
            tarea.from_reqparse(newdata)
            tarea.save_to_db()
            return tarea.json()            

    @swag_from('../swagger/product/delete_product.yaml')
    def delete(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            tarea.delete_from_db()
        
        return {'message': 'El producto se ha eliminido exitosamente'}


class TaskList(Resource):
    @swag_from('../swagger/product/getAll.yaml')
    def getAll(self):
        query = TaskModel.query
        return paginated_results(query)

    @swag_from('../swagger/product/post_product.yaml')
    def post(self):
        data = Task.parser.parse_args()

        tarea = TaskModel(**data)

        try:
            tarea.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'Ocurrió un error al agregar el producto'}

        return tarea.json(), 201

class TaskSearch(Resource):
    @swag_from('../swagger/product/search_product.yaml')
    def post(self):
        query = TaskModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: TaskModel.id == x)
            query = restrict(query,filtros,'descrip',lambda x: TaskModel.descrip.contains(x))
            query = restrict(query,filtros,'status',lambda x: TaskModel.status.contains(x))
            #logica de filtrado de datos 
        return paginated_results(query)
    