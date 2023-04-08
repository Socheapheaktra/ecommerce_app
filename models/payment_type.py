from db import db

from typing import List

class PaymentTypeModel(db.Model):
    __tablename__ = "payment_type"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    user_payment_methods = db.relationship(
        "UserPaymentMethodModel",
        back_populates="payment_type",
        cascade="all, delete",
        lazy="dynamic",
    )

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def find_all(cls) -> List["PaymentTypeModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "PaymentTypeModel":
        return cls.query.get_or_404(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()