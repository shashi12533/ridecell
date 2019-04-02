from flask import Flask
from config import get_config
from models import session
from resources import create_restful_api
from flask_jwt_extended import JWTManager
__author__ = 'shashi'

config = get_config()


def create_app(**kwargs):

    app = Flask(config.FLASK_APP_NAME)

    app.config.from_object(config)
    app.config['JWT_SECRET_KEY'] = 'shashi'
    jwt = JWTManager(app)

    if kwargs.get('rest'):
        create_restful_api(app)

    # TODO This should be somewhere else but here
    def close_session(response_or_exc):
        session.remove()
        return response_or_exc
    app.teardown_appcontext(close_session)
    # app.teardown_request(close_session)
    return app


run_app = create_app(rest=True)
