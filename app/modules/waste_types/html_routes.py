from flask import Blueprint, render_template, request, redirect, url_for
from app.modules.waste_types.models import WasteType
from app.db import db

waste_types_html_bp = Blueprint('waste_types_html_bp', __name__, template_folder='../../templates/waste_types', url_prefix='/ui/waste-types')

@waste_types_html_bp.route('/')
def list_waste_types():
    waste_types = WasteType.query.all()
    return render_template('list.html', waste_types=waste_types)

@waste_types_html_bp.route('/add', methods=['GET', 'POST'])
def add_waste_type_form():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        price_per_unit = float(request.form['price_per_unit'])

        new_waste_type = WasteType(name=name, description=description, price_per_unit=price_per_unit)
        db.session.add(new_waste_type)
        db.session.commit()
        return redirect(url_for('waste_types_html_bp.list_waste_types'))
    return render_template('add_edit.html', waste_type=None)

@waste_types_html_bp.route('/edit/<int:waste_type_id>', methods=['GET', 'POST'])
def edit_waste_type_form(waste_type_id):
    waste_type = WasteType.query.get_or_404(waste_type_id)
    if request.method == 'POST':
        waste_type.name = request.form['name']
        waste_type.description = request.form.get('description')
        waste_type.price_per_unit = float(request.form['price_per_unit'])
        db.session.commit()
        return redirect(url_for('waste_types_html_bp.list_waste_types'))
    return render_template('add_edit.html', waste_type=waste_type)

@waste_types_html_bp.route('/delete/<int:waste_type_id>', methods=['POST'])
def delete_waste_type_action(waste_type_id):
    waste_type = WasteType.query.get_or_404(waste_type_id)
    db.session.delete(waste_type)
    db.session.commit()
    return redirect(url_for('waste_types_html_bp.list_waste_types'))
