from itertools import product
from tkinter import E
from models.product import CatModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request

from utils import paginated_results, _assign_if_something, restrict

class CatList(Resource):
    @swag_from('../swagger/product/category/getAllCat.yaml') 
    def get(self):
        query = CatModel.query
        return paginated_results(query)
