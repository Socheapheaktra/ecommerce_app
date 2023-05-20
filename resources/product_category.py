from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.product_category_schema import ProductCategorySchema, PlainProductCategorySchema

from models.product_category import ProductCategory as Category

from utils.helper import Response

blp = Blueprint("Product Category", __name__, description="Operations on Product Category")

@blp.route('/product_category')
class ProductCategory(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(PlainProductCategorySchema, many=True))
    def get(self):
        """Return List of available Product Categories"""
        try:
            product_categories = Category.find_all()
            return Response(data=product_categories)
        except SQLAlchemyError:
            return Response.server_error()

    @jwt_required()
    @blp.arguments(PlainProductCategorySchema)
    @blp.response(201, responseSchema(ProductCategorySchema))
    def post(self, data):
        """Add new Product Category to database"""
        try:
            # Check Admin's Privillege
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            category_id = data['parent_category_id'] if 'parent_category_id' in data else None
            
            # Check if Parent Category exists
            if category_id:
                parent_category = Category.find_by_id(id=category_id)
                if not parent_category:
                    return Response.not_found(message="Invalid Parent Category ID.")

            product_category = Category(**data)
            product_category.save_to_db()
            return Response.created(
                data=product_category,
                message="Successfully added Product Category.",
            )
        except IntegrityError:
            return Response.bad_request(message="Category name already exists.")
        except SQLAlchemyError:
            return Response.server_error()

@blp.route('/product_category/<int:id>')
class ProductCategoryDetail(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(ProductCategorySchema))
    def get(self, id):
        """Return Information of the Product Category based on ID"""
        try:
            product_category = Category.find_by_id(id=id)
            if not product_category:
                return Response.not_found(message="Invalid Product Category ID.")
            return Response(data=product_category)
        except:
            return Response.server_error()
    
    @jwt_required()
    @blp.response(200, BaseResponseSchema)
    def delete(self, id):
        """Delete Product Category based on ID"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            product_category = Category.find_by_id(id=id)
            if not product_category:
                return Response.not_found("Invalid Product Category ID")
            product_category.delete_from_db()
            return Response(
                data=product_category,
                message="Successfully deleted Product Category."
            )
        except SQLAlchemyError:
            return Response.server_error()