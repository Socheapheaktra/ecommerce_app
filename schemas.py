from marshmallow import Schema, fields

class UserLoginSchema(Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, load_only=True)

class PlainUserSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    email_address = fields.Email(required=True, allow_none=False)
    phone_number = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, load_only=True)
    status = fields.Boolean(required=True, allow_none=False, dump_only=True)

class PlainRoleSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    name = fields.Str(required=True, allow_none=False)

class PlainAddressSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    street_number = fields.Str(required=True, allow_none=False)
    address_line1 = fields.Str(required=True, allow_none=False)
    address_line2 = fields.Str(required=True, allow_none=True)
    city = fields.Str(required=True, allow_none=False)
    region = fields.Str(required=True, allow_none=False)
    postal_code = fields.Str(required=True, allow_none=False)

class PlainCountrySchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    country_name = fields.Str(required=True, allow_none=False)

class CountrySchema(PlainCountrySchema):
    addresses = fields.List(fields.Nested(PlainAddressSchema()), dump_only=True)

class UserSchema(PlainUserSchema):
    role_id = fields.Int(required=True, allow_none=False, dump_only=True)
    role = fields.Nested(PlainRoleSchema(), dump_only=True)
    addresses = fields.List(fields.Nested(PlainAddressSchema()), dump_only=True)

class RoleSchema(PlainRoleSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class AddressSchema(PlainAddressSchema):
    country_id = fields.Int(required=True, allow_none=False)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class UserAndAddressSchema(Schema):
    message = fields.Str(required=True, dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    address = fields.Nested(PlainAddressSchema(), dump_only=True)

class UpdatePasswordSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    old_password = fields.Str(required=True, allow_none=False, load_only=True)
    new_password = fields.Str(required=True, allow_none=False, load_only=True)
    
    message = fields.Str(required=True, allow_none=False, dump_only=True)

class UpdatePasswordWithEmailSchema(Schema):
    email = fields.Email(required=True, allow_none=False)
    new_password = fields.Str(required=True, allow_none=False, load_only=True)
    
    message = fields.Str(required=True, allow_none=False, dump_only=True)

class UpdateUserRoleSchema(Schema):
    user_id = fields.Int(required=True, allow_none=False, load_only=True)
    role_id = fields.Int(required=True, allow_none=False, load_only=True)