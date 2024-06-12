from flask import Flask
from app.config import load_configurations, configure_logging
from .views import webhook_blueprint
from .models import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    # Load configurations and logging settings
    load_configurations(app)
    configure_logging()

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database1.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import and register blueprints, if any
    app.register_blueprint(webhook_blueprint)

    return app
