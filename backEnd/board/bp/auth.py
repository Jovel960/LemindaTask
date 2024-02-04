from flask import  current_app,jsonify, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import db
from db.models import User

_app = Blueprint('auth', __name__)
def init(app): app.register_blueprint(_app, url_prefix='/auth')

def check_user_password_match(pwd1, pwd2):
    return bcrypt.checkpw(pwd1.encode(), pwd2.encode())

def create_user_password_hash(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

@_app.route('/getuser/<username>')
@login_required
def check(username):
    return db.swcdb.user.get_user(username)
  

@_app.route('/login', methods=["POST"])
def login():
    user_id = request.json["userid"].strip()
    user_pwd = request.json["password"].strip()
    if not (user_id and user_pwd):
        return jsonify({"error":"user_id or password is missing"}), 400
    try:
        userFound = db.swcdb.user.get_user(user_id)
        if not (userFound and check_user_password_match(user_pwd, userFound["hashed_pwd"])):
            return jsonify({'error':'username or password are wrong'}), 400
        login_user(User(user_id=userFound['user_id'], user_name=userFound['user_name'], password=userFound['hashed_pwd']))
        return jsonify({"ok":"user logged in"})
    except Exception as e:
        current_app.logger.error(f"Error: {e.__class__.__name__}: {str(e)}")  
        return jsonify({'error': f'something went wrong: {e.__class__.__name__}'}), 400

@_app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"ok":"user logged out"}), 200
    # logout_user();

@_app.route('/register', methods=["POST"])
def register():
    try:
        username = request.json['userid'].strip()
        name = request.json['username'].strip()
        isUserExists = db.swcdb.user.isUserExists(username)
        if(isUserExists):
            return jsonify({'error':'user already exists'}), 400
        hashed_pwd = create_user_password_hash(request.json.pop('password'))
        user_created = db.swcdb.user.register_user(username,name, hashed_pwd)
        #token is an option instead 
        if(user_created):
            user_record = db.swcdb.user.get_user(username)
            login_user(User(user_id=user_record['user_id'], user_name=user_record['user_name'], password=user_record['hashed_pwd']))
            return jsonify({'ok': 'user created successfully', 'username': username}), 201
        else:
            return jsonify({'error':'something went wrong'}), 400
    except Exception as e:
        # Here, e is the exception object, which you can convert to a string to get the message
        current_app.logger.error(f"Error: {e.__class__.__name__}: {str(e)}")  # This prints the type of the exception and the message
        return jsonify({'error': f'something went wrong: {e.__class__.__name__}'}), 400
    
