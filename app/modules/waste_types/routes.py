from flask import Blueprint, request, jsonify
from app.modules.waste_types.models import WasteType
from app.db import db # Import db from app.db

waste_types_bp = Blueprint('waste_types_bp', __name__, url_prefix='/api/waste-types')

@waste_types_bp.route('/', methods=['POST'])
def create_waste_type():
    data = request.get_json()
    if not data or not 'name' in data or not 'price_per_unit' in data:
        return jsonify({'error': 'Missing name or price_per_unit'}), 400
    try:
        new_waste_type = WasteType(
            name=data['name'],
            description=data.get('description'),
            price_per_unit=float(data['price_per_unit'])
        )
        db.session.add(new_waste_type)
        db.session.commit()
        return jsonify({'message': 'Waste type created', 'id': new_waste_type.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@waste_types_bp.route('/', methods=['GET'])
def get_waste_types():
    try:
        waste_types = WasteType.query.all()
        return jsonify([{'id': wt.id, 'name': wt.name, 'description': wt.description, 'price_per_unit': wt.price_per_unit} for wt in waste_types])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@waste_types_bp.route('/<int:waste_type_id>', methods=['GET'])
def get_waste_type(waste_type_id):
    try:
        waste_type = WasteType.query.get_or_404(waste_type_id)
        return jsonify({'id': waste_type.id, 'name': waste_type.name, 'description': waste_type.description, 'price_per_unit': waste_type.price_per_unit})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@waste_types_bp.route('/<int:waste_type_id>', methods=['PUT'])
def update_waste_type(waste_type_id):
    try:
        waste_type = WasteType.query.get_or_404(waste_type_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        waste_type.name = data.get('name', waste_type.name)
        waste_type.description = data.get('description', waste_type.description)
        waste_type.price_per_unit = float(data.get('price_per_unit', waste_type.price_per_unit))
        db.session.commit()
        return jsonify({'message': f'Waste type {waste_type_id} updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@waste_types_bp.route('/<int:waste_type_id>', methods=['DELETE'])
def delete_waste_type(waste_type_id):
    try:
        waste_type = WasteType.query.get_or_404(waste_type_id)
        db.session.delete(waste_type)
        db.session.commit()
        return jsonify({'message': f'Waste type {waste_type_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
