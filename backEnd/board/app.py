from flask import Flask, request, current_app
from flask_cors import CORS
import bp
from flask_login import LoginManager
from db.models import User
import db
from utilities import (APP_SECRET_KEY, set_app_logger, env)

def create_app():
    _app = Flask(__name__)
    _app.config['SECRET_KEY'] = APP_SECRET_KEY
    CORS(_app, supports_credentials=True)
    set_app_logger(_app)
    login_manager = LoginManager()
    login_manager.init_app(_app)
    _app.logger.info(db.swcdb.create_cols()) #optional
    # example for orel
    # Register blueprints here
    # from bp.auth import (bpname)
    # _app.register_blueprint(bpname, url_prefix="/prefix")
    @_app.before_request
    def log_request_info():
        _app.logger.info(f"Method: {request.method}")
        if request.method == "GET":
            _app.logger.info(f"Parameters: {request.args}")
        elif request.method in ["POST", "PUT", "PATCH"]:
            try:
                _app.logger.info(f"JSON data: {request.json}")
            except Exception as e:
                _app.logger.info("No JSON data")
    @_app.after_request
    def log_response_info(response):
        _app.logger.info(f"Status: {response.status}")
        _app.logger.info(f"Headers: {response.headers}")
        return response 
    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.swcdb.user.get_user(user_id)
        if user_data:
            return User(user_id=user_data['user_id'], user_name=user_data['user_name'], password=user_data['hashed_pwd'])
        return None
    bp.init(_app)
    return _app

app = create_app()
 
@app.route('/', methods=['GET'])
def index():
    return 'Leminda Task'


if __name__ == '__main__':
    app.run(debug=True)