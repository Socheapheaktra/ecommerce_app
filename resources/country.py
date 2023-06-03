from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import CountryModel
from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.country_schema import CountrySchema
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
    @jwt_required()
    @blp.response(200, responseSchema(CountrySchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Countries from database"""
        try:
            countries = CountryModel.find_all()
            return Response(data=countries)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @jwt_required()
    @blp.arguments(CountrySchema)
    @blp.response(201, responseSchema(CountrySchema))
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, country_data):
        """Add new Country record into database"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            if country_data['country_name'] == "":
                return Response.bad_request(message="Country Name cannot be empty!")
            country = CountryModel(**country_data)
            country.save_to_db()
            return Response(
                code=201,
                status="Created",
                message="New Country added successfully.",
                data=country
            )
        except IntegrityError:
            return Response.bad_request(message=INTEGRITY_ERROR)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

@blp.route('/country/<int:country_id>')
class CountryUpdate(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(CountrySchema))
    @blp.alt_response(404, example={"code": 404, "message": COUNTRY_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Errro"})
    def get(self, country_id):
        """Return one record of country from database based on ID"""
        try:
            country = CountryModel.find_by_id(id=country_id)
            if not country:
                return Response.not_found(message=COUNTRY_NOT_FOUND.format(country_id=country_id))
            return Response(data=country)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @jwt_required()
    @blp.response(200, responseSchema(CountrySchema))
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
            return Response(data=country, message=DELETE_SUCCESS)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
