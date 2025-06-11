from app.db import db
from datetime import datetime

# Association table for a many-to-many relationship between CollectionRoute and CollectionSchedule
route_schedules_association = db.Table('route_schedules',
    db.Column('route_id', db.Integer, db.ForeignKey('collection_route.id'), primary_key=True),
    db.Column('schedule_id', db.Integer, db.ForeignKey('collection_schedule.id'), primary_key=True)
)

class CollectionRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g., "Route Alpha - 2023-10-26"
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    vehicle = db.relationship('Vehicle', backref=db.backref('routes', lazy=True))

    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True) # Assigned driver/staff
    staff_member = db.relationship('Staff', backref=db.backref('routes', lazy=True))

    route_date = db.Column(db.Date, nullable=False)

    # Stores the optimized order of schedule IDs for this route
    # For simplicity, storing as a comma-separated string of schedule IDs.
    # A more robust solution might use a JSON field or a separate ordered association table.
    ordered_schedule_ids = db.Column(db.Text, nullable=True)

    # To store the Google Maps polyline or directions data
    map_polyline = db.Column(db.Text, nullable=True)
    estimated_duration = db.Column(db.String(50), nullable=True) # e.g., "2 hours 30 mins"
    estimated_distance = db.Column(db.String(50), nullable=True) # e.g., "50 km"

    status = db.Column(db.String(50), default='planned') # e.g., 'planned', 'in_progress', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many relationship with CollectionSchedule
    schedules = db.relationship('CollectionSchedule', secondary=route_schedules_association,
                                    lazy='subquery', backref=db.backref('routes', lazy=True))

    def __repr__(self):
        return f'<CollectionRoute {self.name} on {self.route_date}>'
