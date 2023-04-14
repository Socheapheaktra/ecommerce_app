from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import *
from models import RoleModel

blp = Blueprint("Roles", __name__, description="Operations on Role.")

INTEGRITY_ERROR = "Role name already exists."

INVALID_ROLE_ID = "Invalid Role ID"

SELECT_ERROR = "An error occured while fetching data."
INSERT_ERROR = "An error occurred while inserting."
DELETE_ERROR = "An error occurred while deleting record."

DELETE_SUCCESS = "Role {role} has been deleted."

@blp.route('/role')
class RoleOperation(MethodView):
    @blp.response(200, responseSchema(PlainRoleSchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Roles existed in database"""
        try:
            roles = RoleModel.find_all()
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": roles,
                "message": "Query was successful",
            }
            return res

    @blp.arguments(RoleSchema)
    @blp.response(201, responseSchema(PlainRoleSchema))
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, role_data):
        """Add new role into database if not exists"""
        role = RoleModel(**role_data)
        try:
            role.save_to_db()
        except IntegrityError:
            abort(400, message=INTEGRITY_ERROR.format(name=role.name))
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            res = {
                "code": 201,
                "status": "Created",
                "data": role,
                "message": "New Role Created Successfully."
            }
            return res

@blp.route("/role/<int:role_id>")
class RoleUpdate(MethodView):
    @blp.response(200, responseSchema(RoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_ROLE_ID, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, role_id):
        """Return Role Information based on RoleID"""
        try:
            role = RoleModel.find_by_id(id=role_id)
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": role,
                "message": "Query was successful",
            }
            return res

    @blp.response(200, responseSchema(PlainRoleSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_ROLE_ID, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, role_id):
        """Delete Role from database based on RoleID if exists"""
        role = RoleModel.find_by_id(id=role_id)
        try:
            role.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            res = {
                "code": 200,
                "status": "OK",
                "data": role,
                "message": DELETE_SUCCESS.format(role=role.name)
            }
            return res