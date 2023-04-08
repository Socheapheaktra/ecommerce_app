from db import db

from typing import List

class UserPaymentMethodModel(db.Model):
    __tablename__ = "user_payment_method"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("site_user.id"), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey("payment_type.id"), nullable=False)
    provider = db.Column(db.String(80), nullable=True)
    account_number = db.Column(db.String(80), nullable=True)
    expiry_date = db.Column(db.String(10), nullable=True)
    is_default = db.Column(db.Boolean)

    user = db.relationship("UserModel", back_populates="payment_methods")
    payment_type = db.relationship("PaymentTypeModel", back_populates="user_payment_methods")

    def __init__(
        self,
        user_id: int,
        payment_type_id: int,
        provider: str,
        account_number: str,
        expiry_date: str,
        is_default: bool = False,
    ) -> None:
        self.user_id = user_id
        self.payment_type_id = payment_type_id
        self.provider = provider
        self.account_number = account_number
        self.expiry_date = expiry_date
        self.is_default = is_default

    @classmethod
    def find_all(cls, user_id: int) -> List["UserPaymentMethodModel"]:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_id(cls, id: int) -> "UserPaymentMethodModel":
        return cls.query.get_or_404(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()