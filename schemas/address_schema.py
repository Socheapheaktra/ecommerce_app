from marshmallow import Schema, fields
from .country_schema import CountrySchema

class PlainAddressSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    street_number = fields.Str(required=True, allow_none=True)
    address_line1 = fields.Str(required=True, allow_none=False)
    address_line2 = fields.Str(required=True, allow_none=True)
    city = fields.Str(required=True, allow_none=True)
    postal_code = fields.Str(required=True, allow_none=True)

class AddressSchema(PlainAddressSchema):
    country_id = fields.Int(required=True, allow_none=False, load_only=True)
    country = fields.Nested(CountrySchema(), dump_only=True)
