from db import db
from typing import List

user_address = db.Table(
    "user_address",
    db.Column('user_id', db.Integer, db.ForeignKey("site_user.id"), nullable=False),
    db.Column('address_id', db.Integer, db.ForeignKey("address.id"), nullable=False),
    db.Column('is_default', db.Boolean, default=False)
)

class UserModel(db.Model):
    __tablename__ = "site_user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email_address = db.Column(db.String(80), unique=True, nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    role = db.relationship(
        "RoleModel", 
        back_populates="users",
    )
    
    payment_methods = db.relationship(
        "UserPaymentMethodModel",
        back_populates="user",
    )

    addresses = db.relationship(
        "AddressModel", 
        secondary=user_address, 
        back_populates="users", 
        lazy="dynamic",
        cascade="save-update, merge",
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        password: str,
        role_id: int = 1,
        status: bool = 1,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.password = password
        self.role_id = role_id
        self.status = status

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "UserModel":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()