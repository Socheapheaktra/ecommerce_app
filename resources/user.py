from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import *
from models import UserModel, AddressModel

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
    @blp.alt_response(400, example={"code": 400, "message": "string", "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": "string", "staus": "Internal Server Error"})
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
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
    def get(self, user_id):
        """Get User Information based on UserID"""
        return UserModel.find_by_id(id=user_id)

    @blp.arguments(UpdatePasswordSchema)
    @blp.response(200, UpdatePasswordSchema)
    @blp.alt_response(400, example={"code": 400, "message": "Invalid Credential", "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
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

@blp.route('/user/<int:user_id>/address/<int:address_id>')
class LinkUserAndAddress(MethodView):
    @blp.response(201, UserAndAddressSchema)
    @blp.alt_response(400, example={"code": 400, "message": "string", "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": "string", "status": "Internal Server Error"})
    def post(self, user_id, address_id):
        """Link User to one or more addresses"""
        # Check if user exists
        user = UserModel.query.filter_by(id=user_id).first()
        if user is None:
            abort(404, message="User with id={} does not exist.".format(user_id))
        
        # Check if address exists
        address = AddressModel.query.filter_by(id=address_id).first()
        if address is None:
            abort(404, message="Address with id={} does not exist.".format(address_id))
        
        # Check if relationship between user and address already exists
        if address in user.addresses:
            abort(400, message="User with the corresponding address is already linked.")
        
        try:
            user.addresses.append(address)
            user.save_to_db()
        except SQLAlchemyError:
            abort(500, message=INSERT_ERROR)
        else:
            return {
                "message": "Successfully link user with address.",
                "user": user,
                "address": address,
            }

@blp.route('/reset-password')
class UserResetPassword(MethodView):
    @blp.arguments(UpdatePasswordWithEmailSchema)
    @blp.response(200, UpdatePasswordWithEmailSchema)
    @blp.alt_response(400, example={"code": 400, "message": "string", "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": "string", "status": "Internal Server Error"})
    def post(self, user_data):
        abort(501, message="Reset Password by Email is not yet implemented.")
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
    @blp.alt_response(401, example={"code": 401, "message": "string", "status": "Unauthorized"})
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
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
        abort(501, message="User Logout is not yet implemented.")