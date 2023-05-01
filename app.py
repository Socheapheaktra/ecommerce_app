import os
from flask import Flask, jsonify, redirect
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_uploads import configure_uploads, patch_request_class

from db import db

import models, config

from resources.user import blp as UserBlueprint
from resources.role import blp as RoleBlueprint
from resources.country import blp as CountryBlueprint
from resources.address import blp as AddressBlueprint
from resources.payment_type import blp as PaymentTypeBlueprint
from resources.image import blp as ImageBlueprint

from utils.image_helper import IMAGE_SET

api_prefix = f"{config.API_PREFIX}/{config.API_VERSION}"

def create_app():
    # Initialize Flask Application
    app = Flask(__name__)
    CORS(app)

    app.config['UPLOADED_IMAGES_DEST'] = config.UPLOADED_IMAGES_DEST  # define the path to save the image
    app.config['PROPAGATE_EXCEPTIONS'] = config.PROPAGATE_EXCEPTIONS # I have no IDEA WTF this is
    app.config['API_TITLE'] = config.API_TITLE # Name of your API
    app.config['API_VERSION'] = config.API_VERSION # Version of your API
    app.config['OPENAPI_VERSION'] = config.OPENAPI_VERSION # Also Version of your API Documents
    app.config['OPENAPI_URL_PREFIX'] = config.OPENAPI_URL_PREFIX # URL Prefix
    app.config['OPENAPI_SWAGGER_UI_PATH'] = config.OPENAPI_SWAGGER_UI_PATH # API Document's Path
    app.config['OPENAPI_SWAGGER_UI_URL'] = config.OPENAPI_SWAGGER_UI_URL # Swagger API cdn
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI # Connection String to your database
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@localhost/db_name" # Connection String to your database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS # Also no idea wtf this is

    db.init_app(app) # Initialize Database
    # migrate = Migrate(app, db) # Migrate Database
    api = Api(app) # Link API

    # Configure ImageUploads
    patch_request_class(app, 10 * 1024 * 1024)  # 10MB max size upload
    configure_uploads(app, IMAGE_SET)  # Need to put this after the app.config
    
    # Randomly Generated SECRET KEY
    app.config['JWT_SECRET_KEY'] = "273400726116270771902746508700512837087"
    jwt = JWTManager(app)

    """
    These methods use to modify the Error response about the Authorization
    """

    # Check if the access token is in BLOCKLIST
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return models.TokenModel.query.filter_by(token=jwt_payload['jti']).first()

    # Return the response if the token has been revoked
    # @jwt.revoked_token_loader
    # def revoked_token_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({
    #             "description": "The access token has been revoked.",
    #             "error": "token_revoked"
    #         }),
    #         401
    #     )

    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({
    #             "description": "The token is not fresh.",
    #             "error": "fresh_token_required"
    #         }),
    #         401
    #     )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Do sth in database to verify whether the user is admin or not
        user = models.UserModel.find_by_id(id=identity)
        if user.role.name.lower() == "administrator":
            return {"is_admin": True}

        return {"is_admin": False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({
            "message": "The token has expired.", 
            "error": "token expired."
        }), 401)

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (jsonify({"message": "Signature verification failed.", "error": "invalid token."}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({
            "message": "Missing Access Token.",
            "error": "authorization required."
        }), 401)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint, url_prefix=api_prefix) 
    api.register_blueprint(RoleBlueprint, url_prefix=api_prefix)
    api.register_blueprint(CountryBlueprint, url_prefix=api_prefix)
    api.register_blueprint(AddressBlueprint, url_prefix=api_prefix)
    api.register_blueprint(PaymentTypeBlueprint, url_prefix=api_prefix)
    api.register_blueprint(ImageBlueprint, url_prefix=api_prefix)

    @app.route('/')
    def home():
        return redirect('/swagger-ui')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)