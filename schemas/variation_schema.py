from marshmallow import Schema, fields
from .variation_line_schema import VariationLineSchema
from .product_category_schema import PlainProductCategorySchema

class PlainVariationSchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    name = fields.Str(required=True, allow_none=False)

class VariationSchema(PlainVariationSchema):
    category_id = fields.Int(required=True, allow_none=False, load_only=True)
    category = fields.Nested(PlainProductCategorySchema, dump_only=True)
    variation_lines = fields.Nested(VariationLineSchema(many=True), dump_only=True)