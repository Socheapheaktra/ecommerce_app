from marshmallow import Schema, fields

def responseSchema(parent_schema: Schema = None, many: bool = False):
    class ResponseSchema(BaseResponseSchema):
        data = fields.Nested(parent_schema, many=many, allow_none=True, dump_only=True)
    
    return ResponseSchema

class BaseResponseSchema(Schema):
    code = fields.Int(required=True, allow_none=False, dump_only=True)
    status = fields.Str(required=True, allow_none=False, dump_only=True)
    message = fields.Str(dump_only=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, load_only=True)
    access_token = fields.Str(required=True, allow_none=False, dump_only=True)
    refresh_token = fields.Str(required=True, allow_none=False, dump_only=True)

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

class PlainPaymentTypeSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.String(required=True, allow_none=False)

class PlainUserPaymentMethodSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    user_id = fields.Int(required=True, dump_only=True, allow_none=False)
    payment_type_id = fields.Int(required=True, allow_none=False)
    provider = fields.String(required=True, allow_none=True)
    account_number = fields.String(required=True, allow_none=True)
    expiry_date = fields.String(required=True, allow_none=True)
    is_default = fields.Boolean(required=True, dump_only=True)

class UserPaymentMethodSchema(PlainUserPaymentMethodSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    payment_type = fields.Nested(PlainPaymentTypeSchema(), dump_only=True)

class PaymentTypeSchema(PlainPaymentTypeSchema):
    user_payment_methods = fields.List(fields.Nested(UserPaymentMethodSchema()), dump_only=True)

class CountrySchema(PlainCountrySchema):
    addresses = fields.List(fields.Nested(PlainAddressSchema()), dump_only=True)

class UserSchema(PlainUserSchema):
    role = fields.Nested(PlainRoleSchema(), dump_only=True)
    addresses = fields.List(fields.Nested(PlainAddressSchema()), dump_only=True)
    payment_methods = fields.List(fields.Nested(PlainUserPaymentMethodSchema()), dump_only=True)

class RoleSchema(PlainRoleSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class AddressSchema(PlainAddressSchema):
    country_id = fields.Int(required=True, allow_none=False)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class UserAndAddressSchema(Schema):
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