from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import CountryModel
from schemas import *

blp = Blueprint("Country", __name__, description="Operations on Countries.")

INSERT_ERROR = "An error occurred while inserting data."
INTEGRITY_ERROR = "A country with the name='{}' is already exist."
DELETE_ERROR = "An error occured while deleting data."
DELETE_SUCCESS = "Deleted country name='{country_name}', id='{id}'."

@blp.route('/country')
class CountryOperation(MethodView):
    @blp.response(200, PlainCountrySchema(many=True))
    def get(self):
        """Return List of Countries from database"""
        return CountryModel.find_all()

    @blp.arguments(CountrySchema)
    @blp.response(201, PlainCountrySchema)
    def post(self, country_data):
        """Add new Country record into database"""
        country = CountryModel(**country_data)
        try:
            country.save_to_db()
        except IntegrityError:
            abort(400, INTEGRITY_ERROR.format(country.country_name))
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            return country

@blp.route('/country/<int:country_id>')
class CountryUpdate(MethodView):
    @blp.response(200, CountrySchema)
    def get(self, country_id):
        """Return one record of country from database based on ID"""
        return CountryModel.find_by_id(id=country_id)

    def delete(self, country_id):
        """Delete a country from database based on ID"""
        country = CountryModel.find_by_id(id=country_id)
        try:
            country.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": DELETE_SUCCESS.format(country_name=country.country_name, id=country.id)}