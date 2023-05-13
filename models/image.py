from db import db
from typing import List

class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_item.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    product_item = db.relationship(
        "ProductItem",
        back_populates="image",
    )

    image_lines = db.relationship(
        "ImageLine",
        back_populates="image",
    )

    def __init__(
        self,
        product_item_id: int,
        name: str,
    ) -> None:
        self.product_item_id = product_item_id
        self.name = name

    @classmethod
    def find_all(cls) -> List["Image"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "Image":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()