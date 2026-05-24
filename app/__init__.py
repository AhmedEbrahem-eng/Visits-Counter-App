from flask import Flask
import redis
import os
from app.config import config_by_name

# Global Redis cache client
cache = None

def create_app(config_name=None):
    global cache
    
    if not config_name:
        config_name = os.environ.get("FLASK_ENV", "development")
        
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize redis cache client
    cache = redis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True
    )
    
    # Register blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
