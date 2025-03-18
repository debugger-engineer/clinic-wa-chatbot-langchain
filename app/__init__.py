from flask import Flask
from app.config import Config
from app.utils.logger import setup_logger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize logger
    setup_logger()
    
    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app 