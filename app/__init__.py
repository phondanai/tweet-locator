from flask import Flask
from config import Config
from flask_socketio import SocketIO


socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    socketio.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
