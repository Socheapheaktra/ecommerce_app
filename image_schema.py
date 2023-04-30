from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage
from typing import Mapping

class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            self.fail("invalid")  # raises ValidationError
        
        return value

class ImageSchema(Schema):
    image = FileStorageField(required=True, load_only=True)
    image_url = fields.Str(dump_only=True)