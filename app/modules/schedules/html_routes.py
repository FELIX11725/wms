from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.modules.schedules.models import CollectionSchedule
from app.modules.customers.models import Customer
from app.modules.waste_types.models import WasteType
from app.modules.vehicles.models import Vehicle
from app.modules.staff.models import Staff
from app.db import db
from datetime import datetime

schedules_html_bp = Blueprint('schedules_html_bp', __name__, template_folder='../../templates/schedules', url_prefix='/ui/schedules')

def get_related_data():
    return {
        'customers': Customer.query.all(),
        'waste_types': WasteType.query.all(),
        'vehicles': Vehicle.query.all(),
        'staff_members': Staff.query.all()
    }

@schedules_html_bp.route('/')
def list_schedules():
    schedules = CollectionSchedule.query.order_by(CollectionSchedule.scheduled_date.desc()).all()
    return render_template('list.html', schedules=schedules)

@schedules_html_bp.route('/add', methods=['GET', 'POST'])
def add_schedule_form():
    error = None  # Initialize error to None
    if request.method == 'POST':
        try:
            scheduled_date_str = request.form.get('scheduled_date')
            if not scheduled_date_str:
                flash('Scheduled date is required.', 'error')
                raise ValueError("Scheduled date is required.")

            new_schedule = CollectionSchedule(
                customer_id=request.form.get('customer_id'),
                waste_type_id=request.form.get('waste_type_id'),
                scheduled_date=datetime.strptime(scheduled_date_str, '%Y-%m-%d').date(),
                frequency=request.form.get('frequency'),
                vehicle_id=request.form.get('vehicle_id') if request.form.get('vehicle_id') else None,
                staff_id=request.form.get('staff_id') if request.form.get('staff_id') else None,
                status=request.form.get('status', 'pending'),
                notes=request.form.get('notes')
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('New schedule created successfully!', 'success')
            return redirect(url_for('schedules_html_bp.list_schedules'))
        except ValueError as ve: # Catches date parsing errors or other ValueErrors
            error = str(ve)
            flash(f'Error creating schedule: {error}', 'error')
        except Exception as e:
            db.session.rollback()
            error = str(e)
            flash(f'An unexpected error occurred: {error}', 'error')

        # If POST fails, re-render form with submitted data (if possible) and error
        return render_template('add_edit.html', schedule=request.form, **get_related_data(), error=error)

    return render_template('add_edit.html', schedule=None, **get_related_data(), error=error)

@schedules_html_bp.route('/edit/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule_form(schedule_id):
    schedule = CollectionSchedule.query.get_or_404(schedule_id)
    error = None  # Initialize error to None
    if request.method == 'POST':
        try:
            scheduled_date_str = request.form.get('scheduled_date')
            if not scheduled_date_str:
                flash('Scheduled date is required.', 'error')
                raise ValueError("Scheduled date is required.")

            schedule.customer_id = request.form.get('customer_id')
            schedule.waste_type_id = request.form.get('waste_type_id')
            schedule.scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d').date()
            schedule.frequency = request.form.get('frequency')
            schedule.vehicle_id = request.form.get('vehicle_id') if request.form.get('vehicle_id') else None
            schedule.staff_id = request.form.get('staff_id') if request.form.get('staff_id') else None
            schedule.status = request.form.get('status')
            schedule.notes = request.form.get('notes')

            db.session.commit()
            flash(f'Schedule {schedule_id} updated successfully!', 'success')
            return redirect(url_for('schedules_html_bp.list_schedules'))
        except ValueError as ve:
            error = str(ve)
            flash(f'Error updating schedule: {error}', 'error')
        except Exception as e:
            db.session.rollback()
            error = str(e)
            flash(f'An unexpected error occurred: {error}', 'error')

        return render_template('add_edit.html', schedule=schedule, **get_related_data(), error=error)

    return render_template('add_edit.html', schedule=schedule, **get_related_data(), error=error)

@schedules_html_bp.route('/delete/<int:schedule_id>', methods=['POST'])
def delete_schedule_action(schedule_id):
    schedule = CollectionSchedule.query.get_or_404(schedule_id)
    try:
        db.session.delete(schedule)
        db.session.commit()
        flash(f'Schedule {schedule_id} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting schedule: {str(e)}', 'error')
    return redirect(url_for('schedules_html_bp.list_schedules'))
