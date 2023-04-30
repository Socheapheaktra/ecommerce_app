from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import CountryModel
from schemas import *
from utils.helper import Response

blp = Blueprint("Country", __name__, description="Operations on Countries.")

INTEGRITY_ERROR = "Country already exists."

COUNTRY_NOT_FOUND = "Unable to find Country with ID='{country_id}'"

SELECT_ERROR = "An error occurred while fetcing data."
INSERT_ERROR = "An error occurred while inserting data."
DELETE_ERROR = "An error occured while deleting data."

DELETE_SUCCESS = "Country deleted successfully."

@blp.route('/country')
class CountryOperation(MethodView):
    @blp.response(200, responseSchema(PlainCountrySchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Countries from database"""
        try:
            countries = CountryModel.find_all()
<<<<<<< HEAD
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": countries,
                "message": "Query was successful.",
            }
            return res
=======
            return Response(data=countries)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
>>>>>>> 60dd927c9ea07a781001766f8927689a238119e8

    @blp.arguments(CountrySchema)
    @blp.response(201, responseSchema(PlainCountrySchema))
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, country_data):
        """Add new Country record into database"""
        country = CountryModel(**country_data)
        try:
            country.save_to_db()
            return Response(
                code=201,
                status="Created",
                message="New Country added successfully.",
                data=country
            )
        except IntegrityError:
<<<<<<< HEAD
            abort(400, INTEGRITY_ERROR)
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            res = {
                "code": 201,
                "status": "Created",
                "data": country,
                "message": "New Country {name} added successfully.".format(name=country.country_name)
            }
            return res
=======
            return Response.bad_request(message=INTEGRITY_ERROR)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
>>>>>>> 60dd927c9ea07a781001766f8927689a238119e8

@blp.route('/country/<int:country_id>')
class CountryUpdate(MethodView):
    @blp.response(200, responseSchema(CountrySchema))
    @blp.alt_response(404, example={"code": 404, "message": COUNTRY_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Errro"})
    def get(self, country_id):
        """Return one record of country from database based on ID"""
        try:
            country = CountryModel.find_by_id(id=country_id)
<<<<<<< HEAD
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": country,
                "message": "Query was successful.",
            }
            return res
=======
            if not country:
                return Response.not_found(message=COUNTRY_NOT_FOUND.format(country_id=country_id))
            return Response(data=country)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
>>>>>>> 60dd927c9ea07a781001766f8927689a238119e8

    @blp.response(200, responseSchema(PlainCountrySchema))
    @blp.alt_response(404, example={"code": 404, "message": COUNTRY_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error  "})
    def delete(self, country_id):
        """Delete a country from database based on ID"""
        try:
            # Search Country in database
            country = CountryModel.find_by_id(id=country_id)
            # If not found -> return 404
            if not country:
                return Response.not_found(message=COUNTRY_NOT_FOUND.format(country_id=country_id))

            # If Found -> delete from db and return 200
            country.delete_from_db()
<<<<<<< HEAD
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": country,
                "message": "Country {name} has been deleted successfully.".format(name=country.country_name)
            }
            return res
=======
            return Response(data=country, message=DELETE_SUCCESS)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
>>>>>>> 60dd927c9ea07a781001766f8927689a238119e8
