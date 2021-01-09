from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_assets import Environment

# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()

def create_app():
    """
    instantiate flask app and use flask context to instantiate 
    other dash applications embedded in the flask app
    """
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of Flask App
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.dashboard import create_project1, create_project2
        app = create_project1(app)
        app = create_project2(app)

        # Compile static assets
        compile_static_assets(assets)

        return app
