from db import db
from typing import List

class ShippingMethod(db.Model):
    __tablename__ = "shipping_method"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(
        self,
        name: str,
        price: float,
    ) -> None:
        self.name = name
        self.price = price

    @classmethod
    def find_all(cls) -> List["ShippingMethod"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "ShippingMethod":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()