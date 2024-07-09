#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Restaurant
class Restaurants(Resource):
    def get(self):
        res_dict_list = [restaurant.to_dict(['id','name','address']) for restaurant in Restaurant.query.all()]
        response = make_response(res_dict_list,200)
        return response
    
api.add_resource(Restaurants, '/restaurants')

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant == None:
        res_body = {"error": "Restaurant not found"}
        return make_response(res_body,404)
    
    else:
        if request.method == 'GET':
            rest_dict = restaurant.to_dict()

            response = make_response(rest_dict,200)
            return response
        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()
            response = make_response('',204)
            return response


# Pizzas
class Pizzas(Resource):
    def get(self):
        pizza_dict_list = [pizza.to_dict(['id','name','ingredients']) for pizza in Pizza.query.all()]
        response = make_response(pizza_dict_list,200)
        return response
    
api.add_resource(Pizzas, '/pizzas')

# Restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['GET','POST'])
def rest_pizzas():
    if request.method == 'GET':
        rest_pizzas = []
        for rest_pizza in RestaurantPizza.query.all():
            rp_dict = rest_pizza.to_dict()
            rest_pizzas.append(rp_dict)
        response = make_response(rest_pizzas,200)
        return response
    elif request.method == 'POST':
        try:
            new_rp = RestaurantPizza(
                price = request.form.get("price"),
                pizza_id = request.form.get("pizza_id"),
                restaurant_id = request.form.get("restaurant_id"),
            )
        
            db.session.add(new_rp)
            db.session.commit()
            rest_pizza_dict = new_rp.to_dict()
            response = make_response(rest_pizza_dict,201)
            return response
        
        except Exception as e:
            db.session.rollback()
            res_body={"errors": ["validation errors"]}
            return make_response(res_body,400)
        
        


if __name__ == "__main__":
    app.run(port=5555, debug=True)
