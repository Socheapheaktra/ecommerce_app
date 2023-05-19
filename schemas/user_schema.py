from marshmallow import Schema, fields
from role_schema import RoleSchema
from address_schema import AddressSchema
from payment_type_schema import PaymentTypeSchema

class UserLoginSchema(Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, load_only=True)

class PlainUserSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    email_address = fields.Email(required=True, allow_none=False)
    phone_number = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, load_only=True)
    status = fields.Boolean(required=True, allow_none=False, dump_only=True)

class PlainUserPaymentMethodSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    user_id = fields.Int(required=True, dump_only=True, allow_none=False)
    payment_type_id = fields.Int(required=True, allow_none=False)
    provider = fields.String(required=True, allow_none=True)
    account_number = fields.String(required=True, allow_none=True)
    expiry_date = fields.String(required=True, allow_none=True)
    is_default = fields.Boolean(required=True, dump_only=True)

class UserSchema(PlainUserSchema):
    role = fields.Nested(RoleSchema(), dump_only=True)
    addresses = fields.List(fields.Nested(AddressSchema()), dump_only=True)
    payment_methods = fields.List(fields.Nested(PlainUserPaymentMethodSchema()), dump_only=True)

class UpdatePasswordSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    old_password = fields.Str(required=True, allow_none=False, load_only=True)
    new_password = fields.Str(required=True, allow_none=False, load_only=True)
    
    message = fields.Str(required=True, allow_none=False, dump_only=True)

class UserPaymentMethodSchema(PlainUserPaymentMethodSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    payment_type = fields.Nested(PaymentTypeSchema(), dump_only=True)

class UserAndAddressSchema(Schema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    address = fields.Nested(AddressSchema(), dump_only=True)

class UpdatePasswordWithEmailSchema(Schema):
    email = fields.Email(required=True, allow_none=False)
    new_password = fields.Str(required=True, allow_none=False, load_only=True)
    message = fields.Str(required=True, allow_none=False, dump_only=True)

class UpdateUserRoleSchema(Schema):
    user_id = fields.Int(required=True, allow_none=False, load_only=True)
    role_id = fields.Int(required=True, allow_none=False, load_only=True)