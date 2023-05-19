from marshmallow import Schema, fields

class RoleSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    name = fields.Str(required=True, allow_none=False)