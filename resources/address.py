from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from models import AddressModel, CountryModel
from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.address_schema import PlainAddressSchema, AddressSchema

blp = Blueprint("Addresses", __name__, description="Operations on Addresses.")

INVALID_COUNTRY_ID = "Invalid Country ID"
INVALID_ADDRESS_ID = "Invalid Address ID"

SELECT_ERROR = "An error occurred while fetching address."
INSERT_ERROR = "An error occurred while creating address."
UPDATE_ERROR = "An error occurred while updating address."
DELETE_ERROR = "An error occurred while deleting address."

DELETE_SUCCESS = "Address deleted successfully."

@blp.route('/address')
class AddressList(MethodView):
    @blp.response(200, responseSchema(PlainAddressSchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Get List of Addresses with associated Country"""
        #TODO: remove list of users also return in the response
        try:
            # Equivalent to AddressModel.query.all() 
            addresses = AddressModel.find_all()
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "message": "Query was successful",
                "data": addresses
            }
            return res

    @blp.arguments(AddressSchema)
    @blp.response(201, responseSchema(PlainAddressSchema))
    @blp.alt_response(400, example={"code": 400, "message": INVALID_COUNTRY_ID, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, address_data):
        """Add new Address into the database"""
        country = CountryModel.query.filter_by(id=address_data['country_id']).first()
        if country is None:
            abort(400, message=INVALID_COUNTRY_ID.format(address_data['country_id']))
        
        address = AddressModel(**address_data)
        try:
            address.save_to_db()
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            res = {
                "code": 201,
                "status": "Created",
                "message": "New addresss added successfully",
                "data": address,
            }
            return res

@blp.route('/address/<int:address_id>')
class AddressItem(MethodView):
    @blp.response(200, responseSchema(AddressSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_ADDRESS_ID, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, address_id):
        """Get Address information based on address_id"""
        try:
            address = AddressModel.find_by_id(id=address_id)
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "message": "Query was successful",
                "data": address
            }
            return res

    @blp.arguments(AddressSchema)
    @blp.response(200, responseSchema(AddressSchema))
    @blp.alt_response(400, example={"code": 400, "message": INVALID_COUNTRY_ID, "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": INVALID_ADDRESS_ID, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": UPDATE_ERROR, "status": "Internal Server Error"})
    def put(self, address_data, address_id):
        """Update Address information based on address_id"""
        country = CountryModel.query.filter_by(id=address_data['country_id']).first()
        if country is None:
            abort(400, message=INVALID_COUNTRY_ID)

        address = AddressModel.find_by_id(id=address_id)
        address.address_line1 = address_data['address_line1']
        address.address_line2 = address_data['address_line2']
        address.city = address_data['city']
        address.country_id = address_data['country_id']
        address.postal_code = address_data['postal_code']
        address.region = address_data['region']
        address.street_number = address_data['street_number']
        try:
            address.save_to_db()
        except SQLAlchemyError:
            abort(500, message=UPDATE_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "message": "Update successful on address_id = {addr_id}.".format(addr_id=address.id),
                "data": address
            }
            return res

    @blp.response(200, responseSchema(PlainAddressSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_ADDRESS_ID, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, address_id):
        """Delete Address Record from database based on address_id"""
        address = AddressModel.find_by_id(id=address_id)
        try:
            address.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "message": "Address Deleted Successfully.",
                "data": address,
            }
            return res