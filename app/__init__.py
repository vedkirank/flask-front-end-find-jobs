from flask import Flask
from config import config

# flask shell 
# pip freeze > requirements.txt
# pip install -r requirements.txt


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
