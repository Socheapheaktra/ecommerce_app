from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt, jwt_required

from sqlalchemy.exc import SQLAlchemyError

from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.variation_schema import (
    PlainVariationSchema,
    PlainVariationLineSchema,
    VariationSchema,
    VariationLineSchema
)

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

@blp.route('/variation_line')
class ProductVariationLineController(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(PlainVariationLineSchema, many=True))
    def get(self):
        """Return List of Available Variation Lines"""
        try:
            variation_lines = VariationLine.find_all()
            return Response(data=variation_lines)
        except SQLAlchemyError:
            return Response.server_error()
    
    @jwt_required()
    @blp.arguments(VariationLineSchema)
    @blp.response(201, responseSchema(VariationLineSchema))
    def post(self, data):
        """Add new Variation Line to a parent Variation"""
        try:
            # Check user's privillege
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            
            # Check if Parent Variation Exists
            parent_variation = Variation.find_by_id(id=data['variation_id'])
            if not parent_variation:
                return Response.not_found(message="Invalid Parent Variation ID")
            
            variation_line = VariationLine(**data)
            variation_line.save_to_db()
            return Response.created(
                data=variation_line,
                message="Successfully added Variation Line",
            )
        except SQLAlchemyError:
            return Response.server_error()

@blp.route('/variation_line/<int:id>')
class ProductVariationLineDetailController(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(VariationLineSchema))
    def get(self, id):
        """Get Variation Line detail based on ID"""
        try:
            variation_line = VariationLine.find_by_id(id=id)
            if not variation_line:
                return Response.not_found(message="Invalid Variation Line ID")
            return Response(variation_line)
        except SQLAlchemyError:
            return Response.server_error()
    
    @jwt_required()
    @blp.response(200, BaseResponseSchema)
    def delete(self, id):
        """Delete Variation Line based on ID"""
        try:
            # Check user's privillege
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            
            variation_line = VariationLine.find_by_id(id=id)
            if not variation_line:
                return Response.not_found(message="Invalid Variation Line ID")
            
            variation_line.delete_from_db()
            return Response(
                data=variation_line,
                message="Successfully deleted Variation Line."
            )
        except SQLAlchemyError:
            return Response.server_error()