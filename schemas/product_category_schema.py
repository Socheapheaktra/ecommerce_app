from marshmallow import Schema, fields

class PlainProductCategorySchema(Schema):
    id = fields.Int(required=True, allow_none=False, dump_only=True)
    parent_category_id = fields.Int(load_only=True)
    name = fields.Str(required=True, allow_none=False)

class ProductCategorySchema(PlainProductCategorySchema):
    sub_categories = fields.Nested(PlainProductCategorySchema(many=True), dump_only=True)
