#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = []
        for plant in plants:
            plant_list.append(plant.to_dict())
        return jsonify(plant_list)

    def post(self):
        json_data = request.get_json()
        name = json_data.get('name')
        image = json_data.get('image')  
        price = json_data.get('price')

        
        if not name:
            return make_response(jsonify({"error": "Please provide a name for the plant"}), 400)

        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()

        return jsonify(new_plant.to_dict()), 201


class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict())


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
