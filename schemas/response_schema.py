from marshmallow import Schema, fields

def responseSchema(parent_schema: Schema = None, many: bool = False):
    class ResponseSchema(BaseResponseSchema):
        data = fields.Nested(parent_schema, many=many, allow_none=True, dump_only=True)
    
    return ResponseSchema

class BaseResponseSchema(Schema):
    code = fields.Int(required=True, allow_none=False, dump_only=True)
    status = fields.Str(required=True, allow_none=False, dump_only=True)
    message = fields.Str(dump_only=True)