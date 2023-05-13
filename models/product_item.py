from db import db
from typing import List

class ProductItem(db.Model):
    __tablename__ = "product_item"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    sku = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)

    product = db.relationship(
        "Product",
        back_populates="product_items",
    )

    image = db.relationship(
        "Image",
        back_populates="product_item"
    )

    def __init__(
        self,
        product_id: int,
        price: float,
        sku: str = None,
    ) -> None:
        self.product_id = product_id
        self.sku = sku
        self.price = price

    @classmethod
    def find_all(cls) -> List["ProductItem"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "ProductItem":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()