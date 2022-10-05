from flask import Flask, redirect

from resources.product import Product, ProductList, ProductSearch
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from resources.category import CatList

from db import db

import os

app = Flask(__name__)

api = Api(app, errors={
   ''
})

PREFIX = os.environ.get('PREFIX_PATH', '/api')
 
# Swagger config
app.config['SWAGGER'] = {
   'title': 'catalogue-backend',
   'version': '1.0.0',
   'description': 'API de servicios REST en Flask',
   'uiversion': 2,
   'tags': [{'name': 'jwt'}],
   'specs': [{
       'endpoint': 'apispec_1',
       'route': f'{PREFIX}/apispec_1.json',
       'rule_filter': lambda rule: True,  # all in
       'model_filter': lambda tag: True  # all in
   }],
   'specs_route': f"{PREFIX}/apidocs/",
   'static_url_path': f'{PREFIX}/static'
}
swagger = Swagger(app)

# Function to facilitate the app configuration from environment variables
def env_config(name, default):
   app.config[name] = os.environ.get(name, default=default)

#Database config
env_config('SQLALCHEMY_DATABASE_URI','postgresql://postgres:12345678@localhost:5432/catalogo')

#SQLAlchemy config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False


@app.route('/')
@app.route(f'{PREFIX}')
def welcome():
   return redirect(f"{PREFIX}/apidocs", code=302)
 
api.add_resource(Product, f'{PREFIX}/products/<id>')
api.add_resource(ProductList, f'{PREFIX}/products')
api.add_resource(ProductSearch, f'{PREFIX}/search/products')
api.add_resource(CatList, f'{PREFIX}/categories/')

CORS(app,resources={r'/*':{'origins': '*'}})

# Bloque opcional para ejecutar con python app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run()
else:
    db.init_app(app)