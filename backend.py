"""
REST API CRUD application with Flask, SQL Alchemy, SQLite and marshmallow.
Execute the following lines in python console to create a database :
from backend import db
db.create_all()
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os.path

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

    @property
    def __info(self):
        return f'<{self.id}> {self.name}, price: {self.price}, qty: {self.qty}'

    def __str__(self):
        return self.__info

    def __repr__(self):
        return self.__info

class ProductSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'qty']

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# create a new product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get a product
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# update a product
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):

    product = Product.query.get(id)
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']

    db.session.commit()
    return product_schema.jsonify(product)

# delete a product
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not hasattr(product, 'id'):
        return jsonify({'deleted_product_id': -1})

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)


