from db import db
from typing import List, Union

class AddressModel(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String(80), nullable=False)
    address_line1 = db.Column(db.String(80), nullable=False)
    address_line2 = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.String(80), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)

    country = db.relationship("CountryModel", back_populates="addresses")
    users = db.relationship(
        "UserModel", 
        secondary="user_address", 
        back_populates="addresses", 
        lazy="dynamic",
        cascade="save-update, merge"
    )

    def __init__(
        self,
        street_number: str,
        address_line1: str,
        address_line2: Union[str, None],
        city: str,
        region: str,
        postal_code: str,
        country_id: int,
    ) -> None:
        self.street_number = street_number
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country_id = country_id

    @classmethod
    def find_all(cls) -> List['AddressModel']:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "AddressModel":
        return cls.query.get_or_404(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()