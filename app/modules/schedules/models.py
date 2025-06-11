from app.db import db
from datetime import datetime # For scheduled_date

class CollectionSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('schedules', lazy=True))

    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_type.id'), nullable=False)
    waste_type = db.relationship('WasteType', backref=db.backref('schedules', lazy=True))

    # For simplicity, one vehicle and one primary staff member per schedule.
    # Could be expanded with association tables for many-to-many.
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True) # Nullable if not immediately assigned
    vehicle = db.relationship('Vehicle', backref=db.backref('schedules', lazy=True))

    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True) # Nullable if not immediately assigned
    staff_member = db.relationship('Staff', backref=db.backref('schedules', lazy=True))

    scheduled_date = db.Column(db.Date, nullable=False)
    # Time could be db.Time, or part of a DateTime field if more precision is needed.
    # For now, let's assume daily schedules.
    # scheduled_time = db.Column(db.Time, nullable=True)

    frequency = db.Column(db.String(50)) # e.g., 'once', 'daily', 'weekly', 'monthly'
    status = db.Column(db.String(50), default='pending') # e.g., 'pending', 'assigned', 'completed', 'cancelled'
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CollectionSchedule {self.id} for Customer {self.customer_id} on {self.scheduled_date}>'

# Ensure all related models (Customer, WasteType, Vehicle, Staff) are imported
# before db.create_all() is called if they haven't been implicitly by relationships.
# This is usually handled if their modules are imported in app.py.
