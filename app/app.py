from flask import Flask
from app.db import db

def create_app():
    app = Flask(__name__)
    # It's crucial to set a secret key for session management (e.g., for flash messages)
    app.config['SECRET_KEY'] = 'a_real_secret_key_should_be_set_here_not_this_default'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waste_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register API blueprints
    from app.modules.waste_types.routes import waste_types_bp
    app.register_blueprint(waste_types_bp)
    from app.modules.customers.routes import customers_bp
    app.register_blueprint(customers_bp)
    from app.modules.vehicles.routes import vehicles_bp
    app.register_blueprint(vehicles_bp)
    from app.modules.staff.routes import staff_bp
    app.register_blueprint(staff_bp)
    from app.modules.schedules.routes import schedules_bp
    app.register_blueprint(schedules_bp)
    from app.modules.routes.routes import routes_bp # New
    app.register_blueprint(routes_bp) # New

    # Import and register HTML blueprints
    from app.modules.waste_types.html_routes import waste_types_html_bp
    app.register_blueprint(waste_types_html_bp)
    from app.modules.customers.html_routes import customers_html_bp
    app.register_blueprint(customers_html_bp)
    from app.modules.vehicles.html_routes import vehicles_html_bp
    app.register_blueprint(vehicles_html_bp)
    from app.modules.staff.html_routes import staff_html_bp
    app.register_blueprint(staff_html_bp)
    from app.modules.schedules.html_routes import schedules_html_bp
    app.register_blueprint(schedules_html_bp)

    @app.route('/')
    def hello_world():
        from flask import redirect, url_for
        # For now, redirect to schedules list, will be changed to routes list later
        return redirect(url_for('schedules_html_bp.list_schedules'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
