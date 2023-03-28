from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import *
from models import RoleModel

blp = Blueprint("Roles", __name__, description="Operations on Role.")

INTEGRITY_ERROR = "Role with name of '{name}' already exists."
INSERT_ERROR = "An error occurred while inserting."
DELETE_ERROR = "An error occurred while deleting record."
DELETE_SUCCESS = "Successfully deleted role id='{id}', name='{name}'"

@blp.route('/role')
class RoleOperation(MethodView):
    @blp.response(200, PlainRoleSchema(many=True))
    def get(self):
        """Return List of Roles existed in database"""
        return RoleModel.find_all()

    @blp.arguments(RoleSchema)
    @blp.response(201, PlainRoleSchema)
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
    def get(self, role_id):
        """Return Role Information based on RoleID"""
        return RoleModel.find_by_id(id=role_id)

    def delete(self, role_id):
        """Delete Role from database based on RoleID if exists"""
        role = RoleModel.find_by_id(id=role_id)
        try:
            role.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {"message": DELETE_SUCCESS.format(id=role.id, name=role.name)}