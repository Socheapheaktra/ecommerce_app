from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import *
from models import UserModel, AddressModel, UserPaymentMethodModel
from utils.helper import Response

INTEGRITY_ERROR = "Email Address is already in used."
USER_ADDRESS_INTEGRITY = "User is already linked to the corresponding address."

INVALID_CREDENTIAL = "Invalid user password."

INSERT_ERROR = "An error occurred while creating user."
UPDATE_ERROR = "An error occurred while updating user."
DELETE_ERROR = "An error occurred while deleting user."
SELECT_ERROR = "An error occured while fetching records."

DELETE_COMPLETE = "User {user} has been deleted."
PASSWORD_UPDATE_COMPLETE = "Password updated successfully for user {user}."

ADDRESS_NOT_EXIST = "Address not exist."

INVALID_ADDR_ID = "Invalid Address ID."
INVALID_USER = "Invalid Username."
INVALID_USER_ID = "Invalid User ID."

blp = Blueprint("Users", __name__, description="Operations on Users.")

@blp.route('/user')
class UserOperation(MethodView):
    @blp.response(200, responseSchema(PlainUserSchema, many=True))
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self):
        """Get List of registerd User from database"""
        try:
            users = UserModel.find_all()
            return Response(data=users)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @blp.arguments(UserSchema)
    @blp.response(201, responseSchema(PlainUserSchema))
    @blp.alt_response(400, example={"code": 400, "message": INTEGRITY_ERROR, "status": "Bad Request"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "staus": "Internal Server Error"})
    def post(self, user_data):
        """Register User and add into database"""
        user = UserModel(**user_data)
        try:
            user.save_to_db()
            return Response(
                data=user, 
                code=201, 
                status="Created", 
                message="New User created successfully"
            )
        except IntegrityError:
            return Response(
                code=400,
                status="Bad Request",
                message=INTEGRITY_ERROR
            )
        except SQLAlchemyError as error:
           return Response.server_error(message=error)

@blp.route('/user/<int:user_id>')
class UserUpdate(MethodView):
    @blp.response(200, responseSchema(UserSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_USER, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": SELECT_ERROR, "status": "Internal Server Error"})
    def get(self, user_id):
        """Get User Information based on UserID"""
        try:
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response(code=404, status="Not Found", message=f"Unable to find user with id='{user_id}'")
            else:
                return Response(data=user)
        except SQLAlchemyError as error:
            return Response.server_error(message=error)

    @blp.arguments(UpdatePasswordSchema)
    @blp.response(200, responseSchema(UpdatePasswordSchema()))
    @blp.alt_response(400, example={"code": 400, "message": INVALID_CREDENTIAL, "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": INVALID_USER, "status": "Not Found"})
    def put(self, user_data, user_id):
        try:
            """Update User Password based on UserID"""
            # Check if user exist else return 404
            user = UserModel.find_by_id(id=user_id)
            if user.password != user_data['old_password']:
                abort(400, message=INVALID_CREDENTIAL)
            else:
                user.password = user_data['new_password']
                try:
                    user.save_to_db()
                    return Response(message=PASSWORD_UPDATE_COMPLETE.format(user=user.email_address)).without_data()
                except SQLAlchemyError as error:
                    return Response.server_error(message=error)
        except Exception as error:
            return Response.server_error(message=error)

    @blp.response(200, responseSchema(PlainUserSchema))
    @blp.alt_response(404, example={"code": 404, "message": INVALID_USER, "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": DELETE_ERROR, "status": "Internal Server Error"})
    def delete(self, user_id):
        """Delete User based on UserID if exists"""
        user = UserModel.find_by_id(user_id)
        try:
            user.delete_from_db()
            return Response(data=user, message=DELETE_COMPLETE.format(user=user.email_address))
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

@blp.route('/user/<int:user_id>/payment-method')
class UserPaymentMethod(MethodView):
    @blp.response(200, responseSchema(UserPaymentMethodSchema, many=True))
    def get(self, user_id):
        """Return List of specific user's Payment Method."""
        try:
            payment_methods = UserPaymentMethodModel.find_all(user_id=user_id)
            return Response(data=payment_methods)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @blp.arguments(UserPaymentMethodSchema)
    @blp.response(200, UserPaymentMethodSchema)
    def post(self, data, user_id):
        """Create new User Payment Method."""
        return Response.unimplemented()

@blp.route('/user/<int:user_id>/address/<int:address_id>')
class LinkUserAndAddress(MethodView):
    @blp.response(201, responseSchema(UserAndAddressSchema))
    @blp.alt_response(400, example={"code": 400, "message": USER_ADDRESS_INTEGRITY, "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": "User/Address Not exists.", "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": INSERT_ERROR, "status": "Internal Server Error"})
    def post(self, user_id, address_id):
        try:
            """Link User to one or more addresses"""
            # Check if user exists
            user = UserModel.query.filter_by(id=user_id).first()
            if user is None:
                return Response(
                    code=404,
                    status="Not found",
                    message=INVALID_USER_ID,
                )
            
            # Check if address exists
            address = AddressModel.query.filter_by(id=address_id).first()
            if address is None:
                return Response(
                    code=404,
                    status="Not found",
                    message=INVALID_ADDR_ID
                )
            
            # Check if relationship between user and address already exists
            if address in user.addresses:
                return Response(
                    code=400,
                    status="Bad Request",
                    message=USER_ADDRESS_INTEGRITY,
                )
            
            try:
                user.addresses.append(address)
                user.save_to_db()
                return Response(
                    data={"user": user, "address": address},
                    message="Successfully link user and address."
                )
            except SQLAlchemyError as e:
                return Response.server_error(message=str(e))
        except Exception as error:
            return Response.server_error(message=str(error))

@blp.route('/reset-password')
class UserResetPassword(MethodView):
    @blp.arguments(UpdatePasswordWithEmailSchema)
    @blp.response(200, UpdatePasswordWithEmailSchema)
    @blp.alt_response(400, example={"code": 400, "message": "string", "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": "string", "status": "Not Found"})
    @blp.alt_response(500, example={"code": 500, "message": "string", "status": "Internal Server Error"})
    def post(self, user_data):
        return Response(code=501, status="Not Implemented", message="Sorry, this feature is not yet implemented.")
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
    @blp.response(200, responseSchema(UserSchema))
    @blp.alt_response(401, example={"code": 401, "message": INVALID_CREDENTIAL, "status": "Unauthorized"})
    @blp.alt_response(404, example={"code": 404, "message": INVALID_USER, "status": "Not Found"})
    def post(self, login_data):
        """Return Login Message whethere successful or not"""
        try:
        # Check if User exists
            user = UserModel.query.filter_by(email_address=login_data['email']).first()
            if user is None: # if user not exist
                return Response(
                    code=404,
                    status="Not found",
                    message=INVALID_USER,
                )
            else:
                if user.password != login_data['password']:
                    return Response(
                        code=401,
                        status="Unauthorized",
                        message=INVALID_CREDENTIAL,
                    )
                else:
                    return Response(data=user)
        except SQLAlchemyError as e:
            return Response.server_error(message=str(e))

@blp.route('/logout')
class UserLogout(MethodView):
    @blp.response(200, responseSchema(UserSchema))
    def post(self):
        return Response.unimplemented()