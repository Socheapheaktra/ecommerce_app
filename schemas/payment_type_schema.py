from marshmallow import Schema, fields

class PaymentTypeSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.String(required=True, allow_none=False)