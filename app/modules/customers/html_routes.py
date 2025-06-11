from flask import Blueprint, render_template, request, redirect, url_for
from app.modules.customers.models import Customer
from app.db import db

customers_html_bp = Blueprint('customers_html_bp', __name__, template_folder='../../templates/customers', url_prefix='/ui/customers')

@customers_html_bp.route('/')
def list_customers():
    customers = Customer.query.all()
    return render_template('list.html', customers=customers)

@customers_html_bp.route('/add', methods=['GET', 'POST'])
def add_customer_form():
    if request.method == 'POST':
        try:
            new_customer = Customer(
                name=request.form['name'],
                address=request.form['address'],
                contact_email=request.form['contact_email'],
                contact_phone=request.form.get('contact_phone')
            )
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('customers_html_bp.list_customers'))
        except Exception as e:
            # Simple error handling for now, could flash a message
            db.session.rollback()
            # You might want to pass the error to the template
            return render_template('add_edit.html', customer=None, error=str(e))
    return render_template('add_edit.html', customer=None, error=None)

@customers_html_bp.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer_form(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        try:
            customer.name = request.form['name']
            customer.address = request.form['address']
            customer.contact_email = request.form['contact_email']
            customer.contact_phone = request.form.get('contact_phone')
            db.session.commit()
            return redirect(url_for('customers_html_bp.list_customers'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_edit.html', customer=customer, error=str(e))
    return render_template('add_edit.html', customer=customer, error=None)

@customers_html_bp.route('/delete/<int:customer_id>', methods=['POST'])
def delete_customer_action(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    try:
        db.session.delete(customer)
        db.session.commit()
    except Exception as e:
        # Handle potential errors, e.g., if customer is linked to other records
        db.session.rollback()
        # Ideally, flash a message here
        pass
    return redirect(url_for('customers_html_bp.list_customers'))
