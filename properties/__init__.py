import os

from flask import Flask
from flask_restful import Api

from flask_restful_swagger import swagger


def create_app(test_config=None):
    # Imports
    from . import db
    from properties import resources

    # Creating APP
    app = Flask(__name__, instance_relative_config=True)

    # Creating API
    api = swagger.docs(
        Api(app),
        apiVersion="0.1",
        basePath="http://localhost:8080",
        resourcePath="/",
        produces=["application/json", "text/html"],
        api_spec_url="/api/spec",
        description="API for management of Properties",
    )

    # Configuring APP
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        BUNDLE_ERRORS=True
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure db
    db.init_app(app)

    api.add_resource(resources.Properties, '/properties')
    api.add_resource(resources.Property, '/properties/<string:id>')

    return app
