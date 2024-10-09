#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
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
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'

# Define Resource for Heroes
class HeroResource(Resource):
    def get(self, hero_id):
        hero = Hero.query.get_or_404(hero_id)
        return hero.to_dict(), 200

    def post(self):
        data = request.get_json()
        new_hero = Hero(name=data['name'], super_name=data['super_name'])
        db.session.add(new_hero)
        db.session.commit()
        return new_hero.to_dict(), 201

# Define Resource for Powers
class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get_or_404(power_id)
        return power.to_dict(), 200

    def post(self):
        data = request.get_json()
        new_power = Power(name=data['name'], description=data['description'])
        db.session.add(new_power)
        db.session.commit()
        return new_power.to_dict(), 201

# Register the resources with Flask-RESTful
api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
