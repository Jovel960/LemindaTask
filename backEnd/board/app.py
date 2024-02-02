from flask import Flask
from bp import (auth, questions)
from flask_login import LoginManager
from db.models import User
import db
from utilities.config import APP_SECRET_KEY

def create_app():
    app = Flask(__name__)
    # app.secret_key = 'your_secret_key'
    app.config['SECRET_KEY'] = APP_SECRET_KEY
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.swcdb.user.get_user(user_id)  # This should return a user model instance, not a dict
        if user_data:
            return User(user_id=user_data['user_id'], user_name=user_data['user_name'], password=user_data['hashed_pwd'])
        return None
    app.register_blueprint(auth.app_auth, url_prefix='/auth')
    app.register_blueprint(questions.app_questions)
    @app.route('/', methods=['GET'])
    def index():
        return 'Leminda Task'
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)