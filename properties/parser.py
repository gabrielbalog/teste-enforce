from flask_restful.reqparse import RequestParser

get = RequestParser()
get.add_argument('enrollment', type=str, location='args')
get.add_argument('kind', type=str, location='args')
get.add_argument('area', type=str, location='args')
get.add_argument('area__max', type=str, location='args')
get.add_argument('area__min', type=str, location='args')
get.add_argument('address', type=str, location='args')

create = RequestParser()
create.add_argument('enrollment', required=True,
                    help="The field Enrollmente is required.")
create.add_argument('kind', required=True, help="The field Kind is required.")
create.add_argument('area', required=True, help="The field Area is required.")
create.add_argument('address', required=True,
                    help="Address is required to fill up Latitude and Longitude.")
create.add_argument('unit_measure',
                    choices=('M2', 'Ha'),
                    help="The unit of measure is use to computed the value for the area. {error_msg}")

update = RequestParser()
update.add_argument('enrollment')
update.add_argument('kind')
update.add_argument('area')
update.add_argument('address')
