from flask import Blueprint, request, jsonify
from app.modules.routes.models import CollectionRoute, route_schedules_association
from app.modules.schedules.models import CollectionSchedule
from app.modules.vehicles.models import Vehicle
from app.modules.staff.models import Staff
from app.db import db
from datetime import datetime

routes_bp = Blueprint('routes_bp', __name__, url_prefix='/api/routes')

@routes_bp.route('/', methods=['POST'])
def create_route():
    data = request.get_json()
    required_fields = ['name', 'vehicle_id', 'route_date', 'schedule_ids']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

    if not Vehicle.query.get(data['vehicle_id']):
        return jsonify({'error': 'Vehicle not found'}), 404
    if data.get('staff_id') and not Staff.query.get(data['staff_id']):
        return jsonify({'error': 'Staff not found'}), 404

    schedules = []
    if not isinstance(data['schedule_ids'], list) or not data['schedule_ids']:
        return jsonify({'error': 'schedule_ids must be a non-empty list'}), 400

    for schedule_id in data['schedule_ids']:
        schedule = CollectionSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'error': f'Schedule with id {schedule_id} not found'}), 404
        schedules.append(schedule)

    try:
        new_route = CollectionRoute(
            name=data['name'],
            vehicle_id=data['vehicle_id'],
            staff_id=data.get('staff_id'),
            route_date=datetime.strptime(data['route_date'], '%Y-%m-%d').date(),
            ordered_schedule_ids=data.get('ordered_schedule_ids'), # This would be set after optimization
            map_polyline=data.get('map_polyline'),
            estimated_duration=data.get('estimated_duration'),
            estimated_distance=data.get('estimated_distance'),
            status=data.get('status', 'planned')
        )
        new_route.schedules.extend(schedules) # Add schedules to the route

        db.session.add(new_route)
        db.session.commit()
        return jsonify({'message': 'Route created', 'id': new_route.id}), 201
    except ValueError as ve:
        return jsonify({'error': f'Invalid date format for route_date. Use YYYY-MM-DD. Details: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@routes_bp.route('/', methods=['GET'])
def get_routes():
    try:
        routes = CollectionRoute.query.all()
        result = []
        for r in routes:
            result.append({
                'id': r.id, 'name': r.name,
                'vehicle_id': r.vehicle_id,
                'vehicle_reg': r.vehicle.registration_number if r.vehicle else None,
                'staff_id': r.staff_id,
                'staff_name': r.staff_member.name if r.staff_member else None,
                'route_date': r.route_date.isoformat(),
                'ordered_schedule_ids': r.ordered_schedule_ids,
                'map_polyline': bool(r.map_polyline), # Just indicate if polyline exists
                'estimated_duration': r.estimated_duration,
                'estimated_distance': r.estimated_distance,
                'status': r.status,
                'schedules': [{'id': s.id, 'customer_id': s.customer_id, 'address': s.customer.address if s.customer else 'N/A'} for s in r.schedules]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route('/<int:route_id>', methods=['GET'])
def get_route(route_id):
    try:
        r = CollectionRoute.query.get_or_404(route_id)
        return jsonify({
            'id': r.id, 'name': r.name,
            'vehicle_id': r.vehicle_id,
            'vehicle_reg': r.vehicle.registration_number if r.vehicle else None,
            'staff_id': r.staff_id,
            'staff_name': r.staff_member.name if r.staff_member else None,
            'route_date': r.route_date.isoformat(),
            'ordered_schedule_ids': r.ordered_schedule_ids,
            'map_polyline': r.map_polyline, # Send full polyline for single view
            'estimated_duration': r.estimated_duration,
            'estimated_distance': r.estimated_distance,
            'status': r.status,
            'schedules': [{'id': s.id, 'customer_id': s.customer_id,
                           'customer_name': s.customer.name if s.customer else 'N/A',
                           'address': s.customer.address if s.customer else 'N/A', # Crucial for mapping
                           'waste_type': s.waste_type.name if s.waste_type else 'N/A'} for s in r.schedules]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route('/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    route = CollectionRoute.query.get_or_404(route_id)
    data = request.get_json()
    if not data: return jsonify({'error': 'No data provided'}), 400

    try:
        if 'vehicle_id' in data and data['vehicle_id'] and not Vehicle.query.get(data['vehicle_id']):
            return jsonify({'error': 'Vehicle not found'}), 404
        if 'staff_id' in data and data['staff_id'] and not Staff.query.get(data['staff_id']):
             return jsonify({'error': 'Staff not found'}), 404

        route.name = data.get('name', route.name)
        route.vehicle_id = data.get('vehicle_id', route.vehicle_id)
        route.staff_id = data.get('staff_id', route.staff_id)
        if 'route_date' in data:
            route.route_date = datetime.strptime(data['route_date'], '%Y-%m-%d').date()

        route.ordered_schedule_ids = data.get('ordered_schedule_ids', route.ordered_schedule_ids)
        route.map_polyline = data.get('map_polyline', route.map_polyline)
        route.estimated_duration = data.get('estimated_duration', route.estimated_duration)
        route.estimated_distance = data.get('estimated_distance', route.estimated_distance)
        route.status = data.get('status', route.status)

        if 'schedule_ids' in data:
            schedules = []
            if not isinstance(data['schedule_ids'], list):
                return jsonify({'error': 'schedule_ids must be a list'}), 400
            for schedule_id in data['schedule_ids']:
                schedule = CollectionSchedule.query.get(schedule_id)
                if not schedule: return jsonify({'error': f'Schedule {schedule_id} not found'}), 404
                schedules.append(schedule)
            route.schedules = schedules # Replace existing schedules for this route

        db.session.commit()
        return jsonify({'message': f'Route {route_id} updated'})
    except ValueError as ve:
        return jsonify({'error': f'Invalid date format. Use YYYY-MM-DD. Details: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@routes_bp.route('/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        route = CollectionRoute.query.get_or_404(route_id)
        # Many-to-many relationships are typically cleared automatically when the parent is deleted,
        # or you can explicitly clear route.schedules = [] before deleting if needed.
        db.session.delete(route)
        db.session.commit()
        return jsonify({'message': f'Route {route_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
