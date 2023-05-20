from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt, jwt_required

from sqlalchemy.exc import SQLAlchemyError

from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.variation_schema import PlainVariationSchema, VariationSchema

from models.variation import Variation
from models.variation_line import VariationLine

from utils.helper import Response

blp = Blueprint("Product Variations", __name__, description="Operations on Product Variations")

@blp.route('/variation')
class ProductVariationController(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(PlainVariationSchema, many=True))
    def get(self):
        """Return List of available Product Variations"""
        try:
            variations = Variation.find_all()
            return Response(data=variations)
        except SQLAlchemyError:
            return Response.server_error()
    
    @jwt_required()
    @blp.arguments(VariationSchema)
    @blp.response(201, responseSchema(VariationSchema))
    def post(self, data):
        """Add new Product Variation to database"""
        try:
            # Check admin's privillege
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            variation = Variation(**data)
            variation.save_to_db()
            return Response.created(
                data=variation,
                message="Successfully added Product Variation.",
            )
        except SQLAlchemyError:
            return Response.server_error()

@blp.route('/variation/<int:id>')
class ProductVairationDetailController(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(VariationSchema))
    def get(self, id):
        """Return Product Variation detail based on ID"""
        try:
            variation = Variation.find_by_id(id=id)
            if not variation:
                return Response.not_found()
            return Response(data=variation)
        except SQLAlchemyError:
            return Response.server_error()
    
    @jwt_required()
    @blp.response(200, BaseResponseSchema)
    def delete(self, id):
        """Delete Product Variation based on ID"""
        try:
            # Check user's privillege
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            
            variation = Variation.find_by_id(id=id)
            if not variation:
                return Response.not_found()
            
            variation.delete_from_db()
            return Response(message="Successfully deleted Product Variation.")
        except SQLAlchemyError:
            return Response.server_error()