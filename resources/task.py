from tkinter import E
from models.task import TaskModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request

from utils import paginated_results, _assign_if_something, restrict

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('descrip', type = str)
    parser.add_argument('status', type = str)

    @swag_from('../swagger/task/getProduct_task.yaml')
    def getProduct(self):
        tarea = TaskModel.find_by_id()
        if tarea:
            return tarea.json()
        return {'message': 'Nein'}, 404        

    @swag_from('../swagger/task/put_task.yaml')
    def put(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            newdata = Task.parser.parse_args()
            tarea.from_reqparse(newdata)
            tarea.save_to_db()
            return tarea.json()            

    @swag_from('../swagger/task/delete_task.yaml')
    def delete(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            tarea.delete_from_db()
        
        return {'message': 'La tarea se ha borrado exitosamente'}


class TaskList(Resource):
    @swag_from('../swagger/task/getAll_task.yaml')
    def getAll(self):
        query = TaskModel.query
        return paginated_results(query)

    @swag_from('../swagger/task/post_task.yaml')
    def post(self):
        data = Task.parser.parse_args()

        tarea = TaskModel(**data)

        try:
            tarea.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'Ocurrió un error al crear la tarea'}

        return tarea.json(), 201

class TaskSearch(Resource):
    @swag_from('../swagger/task/search_task.yaml')
    def post(self):
        query = TaskModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: TaskModel.id == x)
            query = restrict(query,filtros,'descrip',lambda x: TaskModel.descrip.contains(x))
            query = restrict(query,filtros,'status',lambda x: TaskModel.status.contains(x))
            #logica de filtrado de datos 
        return paginated_results(query)