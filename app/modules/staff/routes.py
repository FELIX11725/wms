from flask import Blueprint, request, jsonify
from app.modules.staff.models import Staff
from app.db import db

staff_bp = Blueprint('staff_bp', __name__, url_prefix='/api/staff')

@staff_bp.route('/', methods=['POST'])
def create_staff_member():
    data = request.get_json()
    if not data or not 'name' in data or not 'role' in data:
        return jsonify({'error': 'Missing required fields: name, role'}), 400
    try:
        new_staff_member = Staff(
            name=data['name'],
            role=data['role'],
            contact_email=data.get('contact_email'),
            contact_phone=data.get('contact_phone')
        )
        db.session.add(new_staff_member)
        db.session.commit()
        return jsonify({'message': 'Staff member created', 'id': new_staff_member.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@staff_bp.route('/', methods=['GET'])
def get_staff_members():
    try:
        staff_members = Staff.query.all()
        return jsonify([{
            'id': s.id, 'name': s.name, 'role': s.role,
            'contact_email': s.contact_email, 'contact_phone': s.contact_phone
        } for s in staff_members])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/<int:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    try:
        staff_member = Staff.query.get_or_404(staff_id)
        return jsonify({
            'id': staff_member.id, 'name': staff_member.name, 'role': staff_member.role,
            'contact_email': staff_member.contact_email, 'contact_phone': staff_member.contact_phone
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/<int:staff_id>', methods=['PUT'])
def update_staff_member(staff_id):
    try:
        staff_member = Staff.query.get_or_404(staff_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        staff_member.name = data.get('name', staff_member.name)
        staff_member.role = data.get('role', staff_member.role)
        staff_member.contact_email = data.get('contact_email', staff_member.contact_email)
        staff_member.contact_phone = data.get('contact_phone', staff_member.contact_phone)

        db.session.commit()
        return jsonify({'message': f'Staff member {staff_id} updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@staff_bp.route('/<int:staff_id>', methods=['DELETE'])
def delete_staff_member(staff_id):
    try:
        staff_member = Staff.query.get_or_404(staff_id)
        db.session.delete(staff_member)
        db.session.commit()
        return jsonify({'message': f'Staff member {staff_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
