from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    get_jwt_identity,
    get_jwt,
    jwt_required
)

from schemas.response_schema import responseSchema, BaseResponseSchema
from schemas.token_schema import AccessTokenSchema, RefreshTokenSchema
from schemas.user_schema import *

from models import UserModel, AddressModel, UserPaymentMethodModel, RoleModel
from utils.helper import Response

INTEGRITY_ERROR = "Email Address is already in used."
USER_ADDRESS_INTEGRITY = "User is already linked to the corresponding address."

INVALID_CREDENTIAL = "Invalid Credential"

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
    @jwt_required()
    @blp.response(200, responseSchema(PlainUserSchema, many=True))
    def get(self):
        """Get List of registerd User from database"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            users = UserModel.find_all()
            return Response(data=users)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @jwt_required()
    @blp.arguments(UpdateUserInfoSchema)
    @blp.response(200, responseSchema(PlainUserSchema))
    def put(self, user_data):
        """Update UserInformation of logged in User"""
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response.not_found(message="Invalid UserID")
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.phone_number = user_data['phone_number']
            user.save_to_db()
            return Response(
                data=user,
                message="Your information has been updated successfully."
            )
        except SQLAlchemyError as error:
            return Response.server_error(message=error)

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(201, responseSchema(PlainUserSchema))
    def post(self, user_data):
        """Register User and add into database"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            if 'role_id' in user_data:
                user = UserModel(**user_data)
            else:
                # role_id = user_data['role_id'] if 'role_id' in user_data else 1  # default role="Customer"
                user = UserModel(**user_data, role_id=1)
                
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

@blp.route('/user/detail')
class UserDetail(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(UserSchema))
    def get(self):
        """Get Information of logged in user."""
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(id=user_id)
            return Response(data=user)
        except SQLAlchemyError:
            return Response.server_error()

@blp.route('/user/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, responseSchema(PlainUserSchema))
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
    @jwt_required()
    @blp.response(200, responseSchema(UserSchema))
    def get(self, user_id):
        """Get User Information based on UserID"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response.not_found(message="Invalid User ID")
            else:
                return Response(data=user)
        except SQLAlchemyError as error:
            return Response.server_error(message=error)

    @jwt_required()
    @blp.arguments(UpdateUserSchema)
    @blp.response(200, responseSchema(PlainUserSchema))
    def put(self, user_id, user_data):
        """Update User Information Based on UserID"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response.not_found(message="Invalid User ID")
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.phone_number = user_data['phone_number']
            user.password = user_data['password']
            user.role_id = user_data['role_id']
            user.status = user_data['status']
            user.save_to_db()
            return Response(
                data=user,
                message="Successfully Updated User Information."
            )
        except SQLAlchemyError as error:
            return Response.server_error(message=error)

    @jwt_required()
    @blp.response(200, responseSchema(PlainUserSchema))
    def delete(self, user_id):
        """Delete User based on UserID if exists"""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            user = UserModel.find_by_id(user_id)
            if not user:
                return Response.not_found(message=INVALID_USER_ID)
            if user.role.name.lower() == "administrator":
                return Response.bad_request(message="Cannot delete user with role as 'Administrator'")
            user.delete_from_db()
            return Response(data=user, message=DELETE_COMPLETE.format(user=user.email_address))
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

@blp.route('/user/<int:user_id>/role/<int:role_id>')
class UserUpdateRole(MethodView):
    @jwt_required()
    @blp.response(200, BaseResponseSchema)
    def post(self, user_id, role_id):
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response.not_found(message=f"Unable to get user with id='{user_id}'.")
            
            if user.role.name.lower() == "administrator":
                return Response.bad_request(message="Cannot change role of 'Administrator'.")
            
            role = RoleModel.find_by_id(id=role_id)
            if not role:
                return Response.not_found(message=f"Invalid Role ID.")
            
            user.role_id = role_id
            user.save_to_db()
            return Response(message=f"User {user.email_address} has been assigned as {role.name}.")
        except SQLAlchemyError:
            return Response.server_error()

@blp.route('/user/change-password')
class UserUpdatePassword(MethodView):
    @jwt_required()
    @blp.arguments(UpdatePasswordSchema)
    @blp.response(200, responseSchema(UpdatePasswordSchema()))
    @blp.alt_response(400, example={"code": 400, "message": INVALID_CREDENTIAL, "status": "Bad Request"})
    @blp.alt_response(404, example={"code": 404, "message": INVALID_USER, "status": "Not Found"})
    def put(self, user_data):
        """Change Password of logged in user"""
        try:
            # Get user_id
            user_id = get_jwt_identity()
            """Update User Password based on UserID"""
            # Check if user exist else return 404
            user = UserModel.find_by_id(id=user_id)
            if not user:
                return Response.not_found(message=INVALID_USER_ID)
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

@blp.route('/user/<int:user_id>/payment-method')
class UserPaymentMethod(MethodView):
    @jwt_required()
    @blp.response(200, responseSchema(UserPaymentMethodSchema, many=True))
    def get(self, user_id):
        """Return List of specific user's Payment Method."""
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
            payment_methods = UserPaymentMethodModel.find_all(user_id=user_id)
            return Response(data=payment_methods)
        except SQLAlchemyError as error:
            return Response.server_error(message=str(error))

    @jwt_required()
    @blp.arguments(UserPaymentMethodSchema)
    @blp.response(200, UserPaymentMethodSchema)
    def post(self, data, user_id):
        """Create new User Payment Method."""
        return Response.unimplemented()

@blp.route('/user/<int:user_id>/address/<int:address_id>')
class LinkUserAndAddress(MethodView):
    @jwt_required()
    @blp.response(201, responseSchema(UserAndAddressSchema))
    def post(self, user_id, address_id):
        try:
            cur_user = get_jwt()
            if not cur_user['is_admin']:
                return Response.access_denied()
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
    def post(self, user_data):
        return Response.unimplemented()
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
    @blp.response(200, responseSchema(AccessTokenSchema))
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
                    access_token = create_access_token(identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(identity=user.id)
                    res = {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                    return Response(data=res, message="Logged in successful.")
        except SQLAlchemyError as e:
            return Response.server_error(message=str(e))

@blp.route('/logout')
class UserLogout(MethodView):
    @blp.response(200, responseSchema(UserSchema))
    def post(self):
        return Response.unimplemented()

@blp.route('/refresh')
class UserRefreshToken(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, responseSchema(RefreshTokenSchema))
    def get(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        res = {
            "access_token": access_token,
        }
        return Response(data=res)