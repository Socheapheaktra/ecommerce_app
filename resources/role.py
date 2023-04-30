from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import RoleModel
from schemas import *
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
    @blp.response(200, responseSchema(PlainRoleSchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Roles existed in database"""
        try:
            roles = RoleModel.find_all()
            return Response(data=roles)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @blp.arguments(RoleSchema)
    @blp.response(201, responseSchema(PlainRoleSchema))
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, role_data):
        """Add new role into database if not exists"""
        role = RoleModel(**role_data)
        try:
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
    @blp.response(200, responseSchema(RoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, role_id):
        """Return Role Information based on RoleID"""
        try:
            role = RoleModel.find_by_id(id=role_id)
            if not role:
                return Response.not_found(message=ROLE_NOT_FOUND.format(id=role_id))
            return Response(data=role)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @blp.response(200, responseSchema(PlainRoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, role_id):
        """Delete Role from database based on RoleID if exists"""
        try:
            role = RoleModel.find_by_id(id=role_id)
            if not role:
                return Response.not_found(message=ROLE_NOT_FOUND.format(id=role_id))

            role.delete_from_db()
            return Response(data=role, message=DELETE_SUCCESS)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))
