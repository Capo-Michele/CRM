from app.extensions import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_name = db.Column(db.String(100), nullable=False)
    contacts = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(30), nullable=False)
    deal_price = db.Column(db.Numeric(12, 2), nullable=True, default=0)
    currency = db.Column(db.String(3),  default="BYN")
    stage = db.Column(db.String(20), nullable=False, default="Lead")
    deadline = db.Column(db.String(20), nullable=False, default="No deadline")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)



