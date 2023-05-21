from marshmallow import Schema, fields
from .product_category_schema import PlainProductCategorySchema

class PlainVariationSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    name = fields.Str(required=True, allow_none=False)

class PlainVariationLineSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    name = fields.Str(required=True, allow_none=False)

class VariationSchema(PlainVariationSchema):
    category_id = fields.Int(required=True, allow_none=False, load_only=True)
    category = fields.Nested(PlainProductCategorySchema, dump_only=True)
    variation_lines = fields.Nested(PlainVariationLineSchema(many=True), dump_only=True)


class VariationLineSchema(PlainVariationLineSchema):
    variation_id = fields.Int(required=True, allow_none=False, load_only=True)
    variation = fields.Nested(PlainVariationSchema(), dump_only=True)