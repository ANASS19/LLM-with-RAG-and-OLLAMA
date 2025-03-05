# my_flask_app/App.py
from flask import Flask
from flask_cors import CORS
from my_flask_app.routes.routes import api

class Config:
    DEBUG = True
    TESTING = False

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(api, url_prefix="/api")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])
