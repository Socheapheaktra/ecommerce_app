from db import db

class UserAddressModel(db.Model):
    __tablename__ = "user_address"
    
    user_id = db.Column(db.Integer, db.ForeignKey("site_user.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=False)