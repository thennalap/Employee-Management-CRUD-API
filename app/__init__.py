from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt=JWTManager()

# @jwt.invalid_token_loader
# def invalid_token_callback(error):
#     return jsonify({
#         "error": "Invalid token",
#         "message": error
#     }), 401

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)    
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp
    # rplus_api.init_app(api_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.models import bp as models_bp
    app.register_blueprint(models_bp)

    return app
