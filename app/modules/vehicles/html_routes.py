from flask import Blueprint, render_template, request, redirect, url_for
from app.modules.vehicles.models import Vehicle
from app.db import db

vehicles_html_bp = Blueprint('vehicles_html_bp', __name__, template_folder='../../templates/vehicles', url_prefix='/ui/vehicles')

@vehicles_html_bp.route('/')
def list_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('list.html', vehicles=vehicles)

@vehicles_html_bp.route('/add', methods=['GET', 'POST'])
def add_vehicle_form():
    if request.method == 'POST':
        try:
            capacity = request.form.get('capacity')
            new_vehicle = Vehicle(
                registration_number=request.form['registration_number'],
                type=request.form.get('type'),
                capacity=float(capacity) if capacity else None,
                status=request.form.get('status', 'available')
            )
            db.session.add(new_vehicle)
            db.session.commit()
            return redirect(url_for('vehicles_html_bp.list_vehicles'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_edit.html', vehicle=None, error=str(e))
    return render_template('add_edit.html', vehicle=None, error=None)

@vehicles_html_bp.route('/edit/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle_form(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == 'POST':
        try:
            capacity = request.form.get('capacity')
            vehicle.registration_number = request.form['registration_number']
            vehicle.type = request.form.get('type')
            vehicle.capacity = float(capacity) if capacity else None
            vehicle.status = request.form.get('status')
            db.session.commit()
            return redirect(url_for('vehicles_html_bp.list_vehicles'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_edit.html', vehicle=vehicle, error=str(e))
    return render_template('add_edit.html', vehicle=vehicle, error=None)

@vehicles_html_bp.route('/delete/<int:vehicle_id>', methods=['POST'])
def delete_vehicle_action(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    try:
        db.session.delete(vehicle)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Flash message ideally
        pass
    return redirect(url_for('vehicles_html_bp.list_vehicles'))
