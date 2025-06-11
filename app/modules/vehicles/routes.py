from flask import Blueprint, request, jsonify
from app.modules.vehicles.models import Vehicle
from app.db import db

vehicles_bp = Blueprint('vehicles_bp', __name__, url_prefix='/api/vehicles')

@vehicles_bp.route('/', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not data or not 'registration_number' in data:
        return jsonify({'error': 'Missing required field: registration_number'}), 400
    try:
        new_vehicle = Vehicle(
            registration_number=data['registration_number'],
            type=data.get('type'),
            capacity=data.get('capacity'),
            status=data.get('status', 'available')
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle created', 'id': new_vehicle.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@vehicles_bp.route('/', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicle.query.all()
        return jsonify([{
            'id': v.id, 'registration_number': v.registration_number, 'type': v.type,
            'capacity': v.capacity, 'status': v.status
        } for v in vehicles])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        return jsonify({
            'id': vehicle.id, 'registration_number': vehicle.registration_number, 'type': vehicle.type,
            'capacity': vehicle.capacity, 'status': vehicle.status
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        vehicle.registration_number = data.get('registration_number', vehicle.registration_number)
        vehicle.type = data.get('type', vehicle.type)
        vehicle.capacity = data.get('capacity', vehicle.capacity)
        vehicle.status = data.get('status', vehicle.status)

        db.session.commit()
        return jsonify({'message': f'Vehicle {vehicle_id} updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@vehicles_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': f'Vehicle {vehicle_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
