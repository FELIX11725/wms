from app.db import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # e.g., 'Driver', 'Collector', 'Manager'
    contact_email = db.Column(db.String(120), unique=True, nullable=True)
    contact_phone = db.Column(db.String(20), unique=True, nullable=True)
    # Add a relationship to CollectionSchedule later if needed
    # schedules = db.relationship('CollectionSchedule', backref='staff_member', lazy=True) # Example if one staff per schedule
    # Or a secondary table for many-to-many if multiple staff can be on one schedule.

    def __repr__(self):
        return f'<Staff {self.name} ({self.role})>'
