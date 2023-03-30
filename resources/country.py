from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import CountryModel
from schemas import *

blp = Blueprint("Country", __name__, description="Operations on Countries.")

INTEGRITY_ERROR = "A country with that name is already exist."

COUNTRY_NOT_FOUND = "A country with that ID does not exist."

SELECT_ERROR = "An error occurred while fetcing data."
INSERT_ERROR = "An error occurred while inserting data."
DELETE_ERROR = "An error occured while deleting data."

DELETE_SUCCESS = "Country deleted successfully."

@blp.route('/country')
class CountryOperation(MethodView):
    @blp.response(200, PlainCountrySchema(many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Countries from database"""
        try:
            countries = CountryModel.find_all()
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            return countries

    @blp.arguments(CountrySchema)
    @blp.response(201, PlainCountrySchema)
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, country_data):
        """Add new Country record into database"""
        country = CountryModel(**country_data)
        try:
            country.save_to_db()
        except IntegrityError:
            abort(400, INTEGRITY_ERROR)
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            return country

@blp.route('/country/<int:country_id>')
class CountryUpdate(MethodView):
    @blp.response(200, CountrySchema)
    @blp.alt_response(404, example={"code": 404, "message": COUNTRY_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Errro"})
    def get(self, country_id):
        """Return one record of country from database based on ID"""
        try:
            country = CountryModel.find_by_id(id=country_id)
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            return country

    @blp.response(200, None, example={"message": DELETE_SUCCESS})
    @blp.alt_response(404, example={"code": 404, "message": COUNTRY_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error  "})
    def delete(self, country_id):
        """Delete a country from database based on ID"""
        country = CountryModel.find_by_id(id=country_id)
        try:
            country.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": DELETE_SUCCESS}