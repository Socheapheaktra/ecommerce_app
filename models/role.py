from db import db
from typing import List

class RoleModel(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    users = db.relationship("UserModel", back_populates="role")

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def find_all(cls) -> List["RoleModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "RoleModel":
        return cls.query.get_or_404(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()