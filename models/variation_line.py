from db import db
from typing import List

product_variation = db.Table(
    "product_variation",
    db.Column("product_item_id", db.Integer, db.ForeignKey("product_item.id"), nullable=False),
    db.Column("variation_line_id", db.Integer, db.ForeignKey("variation_line.id"), nullable=False)
)

class VariationLine(db.Model):
    __tablename__ = "variation_line"

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey("variation.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    variation = db.relationship(
        "Variation",
        back_populates="variation_lines",
    )

    def __init__(
        self,
        variation_id: int,
        name: str,
    ) -> None:
        self.variation_id = variation_id
        self.name = name

    @classmethod
    def find_all(cls) -> List["VariationLine"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "VariationLine":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()