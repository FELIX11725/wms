from app.db import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), nullable=False, unique=True)
    type = db.Column(db.String(50)) # e.g., 'Truck', 'Van'
    capacity = db.Column(db.Float) # e.g., in kg or cubic meters
    status = db.Column(db.String(50), default='available') # e.g., 'available', 'in_service', 'maintenance'
    # Add a relationship to CollectionSchedule later if needed
    # schedules = db.relationship('CollectionSchedule', backref='vehicle', lazy=True)

    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'
