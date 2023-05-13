from db import db
from typing import List

class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"))

    products = db.relationship(
        "Product",
        back_populates="category"
    )

    variations = db.relationship(
        "Variation",
        back_populates="category",
    )

    def __init__(
        self,
        name: str
    ) -> None:
        self.name = name

    @classmethod
    def find_all(cls) -> List["ProductCategory"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "ProductCategory":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()