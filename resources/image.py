from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_uploads import UploadNotAllowed
from flask import request

from image_schema import ImageSchema
from utils import image_helper
from utils.helper import Response

image_schema = ImageSchema()

blp = Blueprint("Image", __name__, description="Image Uploads")

@blp.route('/upload-image')
class ImageUpload(MethodView):
    def post(self):
        """
        Used to upload an image file.
        """
        data = image_schema.load(request.files)  # {'image': FileStorage}
        # user_id = get_jwt_identity() # returns the user_id
        folder = f"product_images"  # static/images/product_images

        try:
            image_path = image_helper.save_image(image=data['image'], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": f"Image '{basename}' has been uploaded successfully."}
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": f"Image extension '{extension}' is not allowed."}