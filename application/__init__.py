from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_assets import Environment


# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()

# def create_app():
#     """Initialize the core application."""
#     app = Flask(__name__, instance_relative_config=False)
#     # app.config.from_object('config.Config')

#     # Initialize Plugins
#     db.init_app(app)
#     r.init_app(app)

#     with app.app_context():
#         # Include our Routes
#         from . import routes

#         # Register Blueprints
#         # app.register_blueprint(auth.auth_bp)
#         # app.register_blueprint(admin.admin_bp)

#         return app

def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        # Compile static assets
        compile_static_assets(assets)

        return app

# def create_app():
#     """Construct core Flask application with embedded Dash app."""
#     app = Flask(__name__, instance_relative_config=False)
#     # app.config.from_object('config.Config')

#     with app.app_context():
#         # Import Flask routes
#         from application import routes

#         # Import Dash application
#         from application.plotlydash.dashboard import create_dashboard
#         app = create_dashboard(app)

#         # Compile CSS
#         from application.assets import compile_assets
#         compile_assets(app)

#         return app

