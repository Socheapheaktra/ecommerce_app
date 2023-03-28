from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from models import AddressModel, CountryModel
from schemas import *

blp = Blueprint("Addresses", __name__, description="Operations on Addresses.")

DELETE_ERROR = "An error occurred while deleting data."
DELETE_SUCCESS = "Address deleted on id='{}'"
INVALID_COUNTRY_ID = "No Country with id='{}'"
INSERT_ERROR = "An error occurred while inserting data."
UPDATE_ERROR = "An error occurred while updating address on id={}."

@blp.route('/address')
class AddressList(MethodView):
    @blp.response(200, AddressSchema(many=True))
    def get(self):
        """Get List of Addresses with associated Country"""
        return AddressModel.find_all()

    @blp.arguments(AddressSchema)
    @blp.response(201, AddressSchema)
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
            return address

@blp.route('/address/<int:address_id>')
class AddressItem(MethodView):
    @blp.response(200, AddressSchema)
    def get(self, address_id):
        """Get Address information based on address_id"""
        return AddressModel.find_by_id(id=address_id)

    @blp.arguments(AddressSchema)
    @blp.response(200, AddressSchema)
    def put(self, address_data, address_id):
        """Update Address information based on address_id"""
        country = CountryModel.query.filter_by(id=address_data['country_id']).first()
        if country is None:
            abort(400, message=INVALID_COUNTRY_ID.format(address_data['country_id']))

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
            abort(500, message=UPDATE_ERROR.format(address.id))
        else:
            return address

    def delete(self, address_id):
        """Delete Address Record from database based on address_id"""
        address = AddressModel.find_by_id(id=address_id)
        try:
            address.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": DELETE_SUCCESS.format(address.id)}