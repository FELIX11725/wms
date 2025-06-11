from app.db import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(120), unique=True, nullable=False)
    contact_phone = db.Column(db.String(20))
    # Add a relationship to CollectionSchedule later if needed
    # schedules = db.relationship('CollectionSchedule', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'
