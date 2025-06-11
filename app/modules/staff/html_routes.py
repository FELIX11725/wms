from flask import Blueprint, render_template, request, redirect, url_for
from app.modules.staff.models import Staff
from app.db import db

staff_html_bp = Blueprint('staff_html_bp', __name__, template_folder='../../templates/staff', url_prefix='/ui/staff')

@staff_html_bp.route('/')
def list_staff_members():
    staff_members = Staff.query.all()
    return render_template('list.html', staff_members=staff_members)

@staff_html_bp.route('/add', methods=['GET', 'POST'])
def add_staff_form():
    if request.method == 'POST':
        try:
            new_staff_member = Staff(
                name=request.form['name'],
                role=request.form['role'],
                contact_email=request.form.get('contact_email'),
                contact_phone=request.form.get('contact_phone')
            )
            db.session.add(new_staff_member)
            db.session.commit()
            return redirect(url_for('staff_html_bp.list_staff_members'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_edit.html', member=None, error=str(e))
    return render_template('add_edit.html', member=None, error=None)

@staff_html_bp.route('/edit/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff_form(staff_id):
    member = Staff.query.get_or_404(staff_id)
    if request.method == 'POST':
        try:
            member.name = request.form['name']
            member.role = request.form['role']
            member.contact_email = request.form.get('contact_email')
            member.contact_phone = request.form.get('contact_phone')
            db.session.commit()
            return redirect(url_for('staff_html_bp.list_staff_members'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_edit.html', member=member, error=str(e))
    return render_template('add_edit.html', member=member, error=None)

@staff_html_bp.route('/delete/<int:staff_id>', methods=['POST'])
def delete_staff_action(staff_id):
    member = Staff.query.get_or_404(staff_id)
    try:
        db.session.delete(member)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Flash message ideally
        pass
    return redirect(url_for('staff_html_bp.list_staff_members'))
