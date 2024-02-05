from flask import Flask
import bp
from flask_login import LoginManager
from db.models import User
import db
from utilities import (APP_SECRET_KEY, set_app_logger)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = APP_SECRET_KEY
    set_app_logger(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.swcdb.user.get_user(user_id)
        if user_data:
            return User(user_id=user_data['user_id'], user_name=user_data['user_name'], password=user_data['hashed_pwd'])
        return None
    bp.init(app)
    @app.route('/', methods=['GET'])
    def index():
        return 'Leminda Task'
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)