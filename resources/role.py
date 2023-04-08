from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import *
from models import RoleModel

blp = Blueprint("Roles", __name__, description="Operations on Role.")

INTEGRITY_ERROR = "Role name already exists."

ROLE_NOT_FOUND = "Role with that ID does not exist."

SELECT_ERROR = "An error occured while fetching data."
INSERT_ERROR = "An error occurred while inserting."
DELETE_ERROR = "An error occurred while deleting record."

DELETE_SUCCESS = "Role has been deleted."

@blp.route('/role')
class RoleOperation(MethodView):
    @blp.response(200, PlainRoleSchema(many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Return List of Roles existed in database"""
        try:
            roles = RoleModel.find_all()
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            roles
            
        """
        roles = self.env['user.group'].search([])
        return roles
        """

    @blp.arguments(RoleSchema)
    @blp.response(201, PlainRoleSchema)
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
            return role

@blp.route("/role/<int:role_id>")
class RoleUpdate(MethodView):
    @blp.response(200, RoleSchema)
    @blp.response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, role_id):
        """Return Role Information based on RoleID"""
        try:
            role = RoleModel.find_by_id(id=role_id)
        except SQLAlchemyError:
            abort(500, message=SELECT_ERROR)
        else:
            return role

    @blp.response(200, None, example={"message": DELETE_SUCCESS})
    @blp.alt_response(404, example={"code": 404, "message": ROLE_NOT_FOUND, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, role_id):
        """Delete Role from database based on RoleID if exists"""
        role = RoleModel.find_by_id(id=role_id)
        try:
            role.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": DELETE_SUCCESS}