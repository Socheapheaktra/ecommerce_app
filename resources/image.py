from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_uploads import UploadNotAllowed
from flask import request, send_file

from schemas.image_schema import ImageUploadSchema
from schemas.response_schema import responseSchema, BaseResponseSchema
from config import *

from utils import image_helper
from utils.helper import Response

import traceback
import os

image_schema = ImageUploadSchema()
image_folder = "product_images"  # static/images/product_images

blp = Blueprint("Image", __name__, description="Image Uploads")

@blp.route('/upload-image')
class ImageUpload(MethodView):
    @blp.response(200, BaseResponseSchema)
    @blp.alt_response(400, example=Response.bad_request(message="Image extension not allowed."))
    @blp.alt_response(500, example=Response.server_error(message="Failed to upload image."))
    def post(self):
        """
        Used to upload an image file.
        """
        data = image_schema.load(request.files)  # {'image': FileStorage}
        # user_id = get_jwt_identity() # returns the user_id

        try:
            image_path = image_helper.save_image(image=data['image'], folder=image_folder)
            basename = image_helper.get_basename(image_path)
            return Response(
                message=f"Image '{basename}' has been uploaded successfully."
            ).without_data()
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return Response.bad_request(
                message=f"Image extension '{extension}' is not allowed."
            ).without_data()
        except Exception:
            return Response.server_error(
                message="Fail to upload image."
            ).without_data()
        
@blp.route('/image/url/<string:filename>')
class NetworkImage(MethodView):
    @blp.response(200, responseSchema(ImageUploadSchema))
    @blp.alt_response(400, example=Response.bad_request(message="Illegal filename detected."))
    @blp.alt_response(404, example=Response.not_found(message="Image Not Found"))
    @blp.alt_response(500, example=Response.server_error(message="Unable to get image."))
    def get(self, filename: str):
        if not image_helper.is_filename_safe(file=filename):
            return Response.bad_request(message="Illegal filename detected.")
        
        try:
            image_url = image_helper.get_image_url(filename=filename)
            return Response(data={"image_url": image_url})
        except FileNotFoundError:
            return Response.not_found(message="Image not found.")
        except Exception:
            traceback.print_exc()
            return Response.server_error(message="Unable to get image.")

@blp.route('/image/<string:filename>')
class Image(MethodView):
    def get(self, filename: str):
        if not image_helper.is_filename_safe(file=filename):
            return {"message": "Illegal filename detected."}, 400
        
        try:
            return send_file(image_helper.get_path(filename=filename, folder=image_folder))
        except FileNotFoundError:
            traceback.print_exc()
            return {"message": "Image not found."}, 404


    def delete(self, filename: str):
        if not image_helper.is_filename_safe(file=filename):
            return {"message": "Illegal filename detected."}, 400
        
        try:
            os.remove(image_helper.get_path(filename=filename, folder=image_folder))
        except FileNotFoundError:
            return {"message": "File Not Found."}, 404
        except Exception:
            traceback.print_exc()
            return {"message": "Fail to delete image."}, 500