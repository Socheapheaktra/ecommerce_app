from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import *
from models import UserModel

INSERT_ERROR = "An error occurred while inserting into database."
UPDATE_ERROR = "An error occurred while updating record."
DELETE_ERROR = "An error occurred while deleting from database."
DELETE_COMPLETE = "User deleted successfully on id='{id}', email='{email}'."
INTEGRITY_ERROR = "Email Address='{email}' is already in used."
USER_NOT_EXIST = "User with email='{email}' does not exist."
INVALID_CREDENTIAL = "Invalid user password."

blp = Blueprint("Users", __name__, description="Operations on Users.")

@blp.route('/user')
class UserOperation(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get List of registerd User from database"""
        return UserModel.find_all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Register User and add into database"""
        user = UserModel(**user_data)
        try:
            user.save_to_db()
        except IntegrityError:
            abort(400, message=INTEGRITY_ERROR.format(email=user.email_address))
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            return user

@blp.route('/user/<int:user_id>')
class UserUpdate(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get User Information based on UserID"""
        return UserModel.find_by_id(id=user_id)

    @blp.arguments(UpdatePasswordSchema)
    @blp.response(200, UpdatePasswordSchema)
    def put(self, user_data, user_id):
        """Update User Password based on UserID"""
        # Check if user exist else return 404
        user = UserModel.find_by_id(id=user_id)
        if user.password != user_data['old_password']:
            abort(400, message=INVALID_CREDENTIAL)
        else:
            user.password = user_data['new_password']
            try:
                user.save_to_db()
            except SQLAlchemyError:
                abort(500, message=UPDATE_ERROR)
            else:
                return {"message": "Password updated successfully on user_id='{}'".format(user.id)}

    def delete(self, user_id):
        """Delete User based on UserID if exists"""
        user = UserModel.find_by_id(user_id)
        try:
            user.delete_from_db()
        except SQLAlchemyError:
            abort(500, message=DELETE_ERROR)
        else:
            return {
                "message": DELETE_COMPLETE.format(id=user.id, email=user.email_address)
            }

@blp.route('/reset-password')
class UserResetPassword(MethodView):
    @blp.arguments(UpdatePasswordWithEmailSchema)
    @blp.response(200, UpdatePasswordWithEmailSchema)
    def post(self, user_data):
        """Reset User's Password with email address (Need Email Confirmation)"""
        user = UserModel.query.filter_by(email_address=user_data['email']).first()
        if user is None:
            abort(404, message=USER_NOT_EXIST.format(email=user_data['email']))
        else:
            user.password = user_data['new_password']
            try:
                user.save_to_db()
            except SQLAlchemyError:
                abort(500, UPDATE_ERROR)
            else:
                return {"message": "Password updated successfully on user='{}'".format(user.email_address)}

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(200, UserSchema)
    def post(self, login_data):
        """Return Login Message whethere successful or not"""
        # Check if User exists
        user = UserModel.query.filter_by(email_address=login_data['email']).first()
        if user is None: # if user not exist
            abort(404, message=USER_NOT_EXIST.format(email=login_data['email']))
        else:
            if user.password != login_data['password']:
                abort(401, message=INVALID_CREDENTIAL)
            else:
                return user

@blp.route('/logout')
class UserLogout(MethodView):
    def post(self):
        """Logout using JWT Token"""
        abort(501)