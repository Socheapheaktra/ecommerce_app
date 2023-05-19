from marshmallow import Schema, fields

class RefreshTokenSchema(Schema):
    access_token = fields.Str(required=True, allow_none=False, dump_only=True)

class AccessTokenSchema(RefreshTokenSchema):
    refresh_token = fields.Str(required=True, allow_none=False, dump_only=True)