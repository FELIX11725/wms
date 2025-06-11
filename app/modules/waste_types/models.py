from app.db import db # Import db from app.db

class WasteType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    price_per_unit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<WasteType {self.name}>'
