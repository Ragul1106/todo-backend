from flask import Flask
from flask_cors import CORS
from .db import mysql
from .config import Config
from .routes.tasks import task_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})
    mysql.init_app(app)

    app.register_blueprint(task_bp)

    @app.route('/')
    def home():
        return "✅ Flask API is running!"

    return app
