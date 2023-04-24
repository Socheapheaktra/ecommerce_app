from db import db
from typing import List

class CountryModel(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80), unique=True, nullable=False)

    addresses = db.relationship("AddressModel", back_populates="country", cascade="all, delete")

    def __init__(self, country_name: str) -> None:
        self.country_name = country_name

    @classmethod
    def find_all(cls) -> List["CountryModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "CountryModel":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
