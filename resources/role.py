from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import RoleModel
from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.role_schema import RoleSchema
from utils.helper import Response

blp = Blueprint("Roles", __name__, description="Operations on Role.")

INTEGRITY_ERROR = "Role name already exists."

ROLE_NOT_FOUND = "Unable to find Role with id='{id}'."

SELECT_ERROR = "An error occured while fetching data."
INSERT_ERROR = "An error occurred while inserting."
DELETE_ERROR = "An error occurred while deleting record."

DELETE_SUCCESS = "Role has been deleted successfully."

@blp.route('/role')
class RoleOperation(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(RoleSchema, many=True))
    def get(self):
        """Return List of Roles existed in database"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            roles = RoleModel.find_all()
            return Response(data=roles)
        except SQLAlchemyError:
            return Response.server_error()

    @jwt_required()
    @blp.arguments(RoleSchema)
    @blp.response(201, responseSchema(RoleSchema))
    def post(self, role_data):
        """Add new role into database if not exists"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            role = RoleModel(**role_data)
            role.save_to_db()
            return Response(
                code=201,
                status="Created",
                message="New Role has been created successfully.",
                data=role,
            )
        except IntegrityError:
            return Response(
                code=400,
                status="Bad Request",
                message=INTEGRITY_ERROR,
            )
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

@blp.route("/role/<int:role_id>")
class RoleUpdate(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(RoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, role_id):
        """Return Role Information based on RoleID"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            role = RoleModel.find_by_id(id=role_id)
            if not role:
                return Response.not_found(message=ROLE_NOT_FOUND.format(id=role_id))
            return Response(data=role)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @jwt_required()
    @blp.response(200, responseSchema(RoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, role_id):
        """Delete Role from database based on RoleID if exists"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            role = RoleModel.find_by_id(id=role_id)
            if not role:
                return Response.not_found(message=ROLE_NOT_FOUND.format(id=role_id))

            role.delete_from_db()
            return Response(data=role, message=DELETE_SUCCESS)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
