from marshmallow import Schema, fields

class CountrySchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    country_name = fields.Str(required=True, allow_none=False)