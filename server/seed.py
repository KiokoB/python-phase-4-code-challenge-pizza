#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    db.drop_all()
    db.create_all()
    db.session.remove()
    print("Deleting data...")
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")

    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(
        name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizza...")

    pr1 = RestaurantPizza(price=1, pizza=cheese,restaurant=shack)
    pr2 = RestaurantPizza(price=4, pizza=pepperoni,restaurant=bistro)
    pr3 = RestaurantPizza(price=5, pizza=california,restaurant=palace)
    restaurantPizzas = [pr1, pr2, pr3]
    # pr = RestaurantPizza(price = 5, pizza =cheese, restaurant = bistro)
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurantPizzas)
    # db.session.add_all(pr)
    db.session.commit()

    print("Seeding done!")
