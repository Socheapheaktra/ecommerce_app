from db import db
from typing import List

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))

    category = db.relationship(
        "ProductCategory",
        back_populates="products",
    )

    product_items = db.relationship(
        "ProductItem",
        back_populates="product"
    )

    def __init__(
        self,
        category_id: int,
        name: str,
        description: str = None
    ) -> None:
        self.category_id = category_id
        self.name = name
        self.description = description

    @classmethod
    def find_all(cls) -> List["Product"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "Product":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()