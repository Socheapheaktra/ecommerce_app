from db import db
from typing import List

class Variation(db.Model):
    __tablename__ = "variation"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    category = db.relationship(
        "ProductCategory",
        back_populates="variations",
    )

    variation_lines = db.relationship(
        "VariationLine",
        back_populates="variation"
    )

    def __init__(
        self,
        category_id: int,
        name: str,
    ) -> None:
        self.category_id = category_id
        self.name = name

    @classmethod
    def find_all(cls) -> List["Variation"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "Variation":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()