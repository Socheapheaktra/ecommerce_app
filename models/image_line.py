from db import db
from typing import List

class ImageLine(db.Model):
    __tablename__ = "image_line"

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

    image = db.relationship(
        "Image",
        back_populates="image_lines",
    )

    def __init__(
        self,
        image_id: int,
        image_path: str,
    ) -> None:
        self.image_id = image_id
        self.image_path = image_path

    @classmethod
    def find_all(cls) -> List["ImageLine"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id: int) -> "ImageLine":
        return cls.query.get(id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()