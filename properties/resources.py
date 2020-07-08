import json

from flask_restful import Resource, abort, reqparse
from psycopg2.errors import UniqueViolation

from flask_restful_swagger import swagger
from properties import models
from properties.geocode import gmaps
from properties.parser import create, update


class Properties(Resource):
    @swagger.operation(
        notes="Get All Properties",
        nickname="get",
    )
    def get(self):
        properties = models.Property.query.all()
        return {
            'success': True,
            'count': len(properties),
            'data': [p.json for p in properties]
        }

    @swagger.operation(
        notes="Create a new Property",
        nickname="post",
        parameters=[
            {
              "name": "body",
              "description": "The body data for creation of the property",
              "required": True,
              "allowMultiple": False,
              "dataType": models.Property.__name__,
              "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created. Return a success boolean, and a data key with the property as value."
            },
            {
                "code": 400,
                "message": "Unique value for field"
            }
        ]

    )
    def post(self):
        args = create.parse_args()

        try:
            unit_measure = args.pop('unit_measure')

            if unit_measure == 'Ha':
                # Check to see if the unit is Ha and then convert to M2
                args['area'] = float(args['area']) * 1000

            gr = gmaps.geocode(args.get('address'))
            if gr:
                args['lat'] = gr[0]["geometry"]["location"]["lat"]
                args['lgn'] = gr[0]["geometry"]["location"]["lng"]

            p = models.Property(**args)
            p.save()

            return {
                'success': True,
                'data': p.json
            }, 201

        except Exception as e:
            return {
                'success': False,
                'error': f'An error has ocurred. {e}'[:150]
            }, 400


class Property(Resource):
    @staticmethod
    def get_or_raise(model, id):
        d = model.query.get(id)
        if not d:
            abort(404, message={
                'success': False,
                'error': f'{model.__name__} not found with the id {id}'
            })

        return d

    @swagger.operation(
        notes="Get a given property",
        nickname="get",
        parameters=[
            {
                "name": "id",
                "description": "The ID of the Property item",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Return the item."
            },
            {
                "code": 404,
                "message": "The item weren't found."
            }
        ]

    )
    def get(self, id):
        d = self.get_or_raise(models.Property, id)

        return {
            'success': True,
            'data': d.json
        }

    @swagger.operation(
        notes="Update a given property",
        nickname="post",
        parameters=[
            {
                "name": "id",
                "description": "The ID of the Property item",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            },
            {
                "name": "body",
                "description": "The body data for update the property",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Return the item updated."
            },
            {
                "code": 400,
                "message": "Unique value for field."
            },
            {
                "code": 404,
                "message": "The item weren't found."
            }
        ]

    )
    def put(self, id):
        args = update.parse_args()
        d = self.get_or_raise(models.Property, id)

        try:
            d.update(**args)

            return {
                'success': True,
                'data': d.json
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'An error has ocurred. {e}'[:150]
            }, 400

    @swagger.operation(
        notes="Delete a given property",
        nickname="delete",
        parameters=[
            {
                "name": "id",
                "description": "The ID of the Property item",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Return empty dict meaning that the item was deleted."
            },
            {
                "code": 404,
                "message": "The item weren't found."
            }
        ]

    )
    def delete(self, id):
        d = self.get_or_raise(models.Property, id)
        d.remove()
        return {}, 200
