from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import PaymentTypeModel
from schemas import *

blp = Blueprint(
    "Payment Types",
    __name__,
    description="Operations on Payment Types",
)

SELECT_ERROR = "An error occurred while fetching data."
INSERT_ERROR = "An error occurred while inserting data."
DELETE_ERROR = "An error occurred while deleting data."

INTEGRITY_ERROR = "Payment Type already exist."
INVALID_PAYMENT_TYPE = "Invalid PaymentType ID"

@blp.route('/payment-type')
class PaymentType(MethodView):
    @blp.response(200, PlainPaymentTypeSchema(many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(sefl):
        """Get List of Payment Types"""
        try:
            payment_types = PaymentTypeModel.find_all()
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            return payment_types

    @blp.arguments(PlainPaymentTypeSchema)
    @blp.response(200, PlainPaymentTypeSchema)
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, data):
        """Add new Payment Types into databse if not exist"""
        payment_type = PaymentTypeModel(**data)
        try:
            payment_type.save_to_db()
        except IntegrityError:
            abort(400, message=INTEGRITY_ERROR)
        else:
            return payment_type

@blp.route('/payment-type/<int:payment_type_id>')
class PaymentTypeDetail(MethodView):
    @blp.response(200, PaymentTypeSchema)
    @blp.alt_response(404, example={"code": 404, "message": INVALID_PAYMENT_TYPE, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, payment_type_id):
        """Get Informations of Payment Type based on ID"""
        try:
            payment_type = PaymentTypeModel.find_by_id(id=payment_type_id)
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            return payment_type

    @blp.response(200, example={"message": "Payment Type=<name> has been deleted."})
    @blp.alt_response(404, example={"code": 404, "message": INVALID_PAYMENT_TYPE, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR})
    def delete(self, payment_type_id):
        """Delete existing Payment Type based on ID"""
        payment_type = PaymentTypeModel.find_by_id(id=payment_type_id)
        try:
            payment_type.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": "Payment Type={} has been deleted.".format(payment_type.name)}