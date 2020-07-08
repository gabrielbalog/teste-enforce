from flask import jsonify

from flask_restful_swagger import swagger
from properties.db import db
from properties.utils import to_dict


class CRUDMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

@swagger.model
class Property(db.Model, CRUDMixin):
    """ Model to store that from property.
        It provides the basic for create, update and delete.
        It also returns a JSON representation of its fields.
    """
    __endpoint__ = "property"

    id = db.Column(db.Integer, primary_key=True)
    enrollment = db.Column(db.String(100), nullable=False, unique=True)
    kind = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float(), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float())
    lgn = db.Column(db.Float())

    def __repr__(self):
        return self.enrollment

    @classmethod
    def search_by_enrollment(cls, enrollment):
        return cls.query.filter_by(enrollment=enrollment)

    @property
    def json(self):
        return to_dict(self, self.__class__)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

        self.save()
