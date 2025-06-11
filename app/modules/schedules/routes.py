from flask import Blueprint, request, jsonify
from app.modules.schedules.models import CollectionSchedule
from app.modules.customers.models import Customer # Needed for validation/linking
from app.modules.waste_types.models import WasteType # Needed for validation/linking
from app.modules.vehicles.models import Vehicle # Needed for validation/linking
from app.modules.staff.models import Staff # Needed for validation/linking
from app.db import db
from datetime import datetime

schedules_bp = Blueprint('schedules_bp', __name__, url_prefix='/api/schedules')

@schedules_bp.route('/', methods=['POST'])
def create_schedule():
    data = request.get_json()
    required_fields = ['customer_id', 'waste_type_id', 'scheduled_date', 'frequency']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

    try:
        # Validate foreign keys
        if not Customer.query.get(data['customer_id']):
            return jsonify({'error': 'Customer not found'}), 404
        if not WasteType.query.get(data['waste_type_id']):
            return jsonify({'error': 'WasteType not found'}), 404
        if data.get('vehicle_id') and not Vehicle.query.get(data['vehicle_id']):
            return jsonify({'error': 'Vehicle not found'}), 404
        if data.get('staff_id') and not Staff.query.get(data['staff_id']):
            return jsonify({'error': 'Staff member not found'}), 404

        new_schedule = CollectionSchedule(
            customer_id=data['customer_id'],
            waste_type_id=data['waste_type_id'],
            scheduled_date=datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date(),
            frequency=data['frequency'],
            vehicle_id=data.get('vehicle_id'),
            staff_id=data.get('staff_id'),
            status=data.get('status', 'pending'),
            notes=data.get('notes')
        )
        db.session.add(new_schedule)
        db.session.commit()
        return jsonify({'message': 'Schedule created', 'id': new_schedule.id}), 201
    except ValueError as ve: # Catch issues with date parsing
        return jsonify({'error': f'Invalid date format for scheduled_date. Use YYYY-MM-DD. Details: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@schedules_bp.route('/', methods=['GET'])
def get_schedules():
    try:
        schedules = CollectionSchedule.query.all()
        result = []
        for s in schedules:
            result.append({
                'id': s.id,
                'customer_id': s.customer_id,
                'customer_name': s.customer.name if s.customer else None, # Eager load or handle potential None
                'waste_type_id': s.waste_type_id,
                'waste_type_name': s.waste_type.name if s.waste_type else None,
                'vehicle_id': s.vehicle_id,
                'vehicle_reg': s.vehicle.registration_number if s.vehicle else None,
                'staff_id': s.staff_id,
                'staff_name': s.staff_member.name if s.staff_member else None,
                'scheduled_date': s.scheduled_date.isoformat(),
                'frequency': s.frequency,
                'status': s.status,
                'notes': s.notes,
                'created_at': s.created_at.isoformat()
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schedules_bp.route('/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    try:
        s = CollectionSchedule.query.get_or_404(schedule_id)
        return jsonify({
            'id': s.id,
            'customer_id': s.customer_id,
            'customer_name': s.customer.name if s.customer else None,
            'waste_type_id': s.waste_type_id,
            'waste_type_name': s.waste_type.name if s.waste_type else None,
            'vehicle_id': s.vehicle_id,
            'vehicle_reg': s.vehicle.registration_number if s.vehicle else None,
            'staff_id': s.staff_id,
            'staff_name': s.staff_member.name if s.staff_member else None,
            'scheduled_date': s.scheduled_date.isoformat(),
            'frequency': s.frequency,
            'status': s.status,
            'notes': s.notes,
            'created_at': s.created_at.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schedules_bp.route('/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    s = CollectionSchedule.query.get_or_404(schedule_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        if 'customer_id' in data and not Customer.query.get(data['customer_id']):
                 return jsonify({'error': 'Customer not found'}), 404
        if 'waste_type_id' in data and not WasteType.query.get(data['waste_type_id']):
                 return jsonify({'error': 'WasteType not found'}), 404
        if data.get('vehicle_id') and not Vehicle.query.get(data['vehicle_id']):
            return jsonify({'error': 'Vehicle not found'}), 404
        if data.get('staff_id') and not Staff.query.get(data['staff_id']):
            return jsonify({'error': 'Staff member not found'}), 404

        s.customer_id = data.get('customer_id', s.customer_id)
        s.waste_type_id = data.get('waste_type_id', s.waste_type_id)
        if 'scheduled_date' in data:
            s.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        s.frequency = data.get('frequency', s.frequency)
        s.vehicle_id = data.get('vehicle_id', s.vehicle_id)
        s.staff_id = data.get('staff_id', s.staff_id)
        s.status = data.get('status', s.status)
        s.notes = data.get('notes', s.notes)

        db.session.commit()
        return jsonify({'message': f'Schedule {schedule_id} updated'})
    except ValueError as ve:
        return jsonify({'error': f'Invalid date format for scheduled_date. Use YYYY-MM-DD. Details: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@schedules_bp.route('/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        s = CollectionSchedule.query.get_or_404(schedule_id)
        db.session.delete(s)
        db.session.commit()
        return jsonify({'message': f'Schedule {schedule_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
