#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)  # Initialize Flask-RESTful

# -------------------------------
# Home Route (Just for Testing)
# -------------------------------
@app.route('/')
def index():
    return '<h1>Code Challenge: Pizza Restaurants</h1>'


# -------------------------------
# GET /restaurants (Retrieve all restaurants)
# -------------------------------
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200


# -------------------------------
# GET /restaurants/<id> (Retrieve a restaurant by ID)
# -------------------------------
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        return jsonify(restaurant.to_dict(include_pizzas=True)), 200
    return jsonify({"error": "Restaurant not found"}), 404


# -------------------------------
# DELETE /restaurants/<id> (Delete a restaurant)
# -------------------------------
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204  # No content response
    return jsonify({"error": "Restaurant not found"}), 404


# -------------------------------
# GET /pizzas (Retrieve all pizzas)
# -------------------------------
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200


# -------------------------------
# POST /restaurant_pizzas (Add pizza to a restaurant)
# -------------------------------
@app.route('/restaurant_pizzas', methods=['POST'])
def add_restaurant_pizza():
    try:
        data = request.get_json()

        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify(new_restaurant_pizza.to_dict()), 201

    except ValueError as e:
        return jsonify({"errors": ["validation errors"]}), 400  # 🔥 Fix error message format



if __name__ == '__main__':
    app.run(port=5555, debug=True)
