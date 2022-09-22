from itertools import product
from tkinter import E
from models.product import CatModel, ProductModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request

from utils import paginated_results, _assign_if_something, restrict

class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('descripcion', type = str)
    parser.add_argument('estado', type = str)
    parser.add_argument('nombre', type = str)
    parser.add_argument('precio', type = str)
    parser.add_argument('proveedor_id', type = int)
    parser.add_argument('categoria_id', type = int)

    @swag_from('../swagger/product/get_product.yaml')
    def getProduct(self):
        product = ProductModel.find_by_id()
        if product:
            return product.json()
        return {'message': 'Nein'}, 404        

    @swag_from('../swagger/product/put_product.yaml')
    def put(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            newdata = Product.parser.parse_args()
            product.from_reqparse(newdata)
            product.save_to_db()
            return product.json()            

    @swag_from('../swagger/product/delete_product.yaml')
    def delete(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            product.delete_from_db()
        
        return {'message': 'El producto se ha eliminido exitosamente'}


class ProductList(Resource):
    @swag_from('../swagger/product/getAll.yaml')
    def getAll(self):
        query = ProductModel.query
        return paginated_results(query)

    @swag_from('../swagger/product/post_product.yaml')
    def post(self):
        data = Product.parser.parse_args()

        product = ProductModel(**data)

        try:
            product.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'Ocurrió un error al agregar el producto'}

        return product.json(), 201

class ProductSearch(Resource):
    @swag_from('../swagger/product/search_product.yaml')
    def post(self):
        query = ProductModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: ProductModel.id == x)
            query = restrict(query,filtros,'descripcion',lambda x: ProductModel.descripcion.contains(x))
            query = restrict(query,filtros,'estado',lambda x: ProductModel.estado.contains(x))
            query = restrict(query,filtros,'nombre',lambda x: ProductModel.nombre.contains(x))
            #logica de filtrado de datos 
        return paginated_results(query)

