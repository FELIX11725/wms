from flask import Blueprint, request, jsonify
from app.modules.customers.models import Customer
from app.db import db

customers_bp = Blueprint('customers_bp', __name__, url_prefix='/api/customers')

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or not 'name' in data or not 'address' in data or not 'contact_email' in data:
        return jsonify({'error': 'Missing required fields (name, address, contact_email)'}), 400
    try:
        new_customer = Customer(
            name=data['name'],
            address=data['address'],
            contact_email=data['contact_email'],
            contact_phone=data.get('contact_phone')
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer created', 'id': new_customer.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@customers_bp.route('/', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify([{
            'id': c.id, 'name': c.name, 'address': c.address,
            'contact_email': c.contact_email, 'contact_phone': c.contact_phone
        } for c in customers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify({
            'id': customer.id, 'name': customer.name, 'address': customer.address,
            'contact_email': customer.contact_email, 'contact_phone': customer.contact_phone
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        customer.name = data.get('name', customer.name)
        customer.address = data.get('address', customer.address)
        customer.contact_email = data.get('contact_email', customer.contact_email)
        customer.contact_phone = data.get('contact_phone', customer.contact_phone)

        db.session.commit()
        return jsonify({'message': f'Customer {customer_id} updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': f'Customer {customer_id} deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
