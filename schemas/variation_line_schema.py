from marshmallow import Schema, fields

class VariationLineSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    variation_id = fields.Int(required=True, allow_none=False, load_only=True)
    name = fields.Str(required=True, allow_none=False)