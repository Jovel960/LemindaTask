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
    user = db.swcdb.user.get_user(username)
    if user:
        return jsonify(user), 200
    else: 
        return jsonify({"error":"user not found"}), 400
  

@_app.route('/login', methods=["POST"])
def login():
    if current_user.is_authenticated: 
        return jsonify({'error':'user is already logged in'}), 400
    user_id = request.json.get("userid", '').strip()
    user_pwd = request.json.get("password", '').strip()
    if not (user_id and user_pwd):
        return jsonify({"error":"user_id or password is missing"}), 400
    try:
        userFound = db.swcdb.user.get_user(user_id)
        if not (userFound and check_user_password_match(user_pwd, userFound["hashed_pwd"])):
            return jsonify({'error':'username or password are wrong'}), 400
        login_user(User(user_id=userFound['user_id'], user_name=userFound['user_name'], password=userFound['hashed_pwd']))
        return jsonify({"ok":"user logged in"}), 200
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
        user_id = request.json.get('userid', '').strip()
        name = request.json.get('username', '').strip()
        user_pwd = request.json.get('password', '').strip()
        if not (user_id and user_pwd and name):
            return jsonify({'error':'username, name and password must be provided'}), 400 
        if len(user_id) < 3 or len(user_pwd) < 3 or len(name) < 3:
            return jsonify({'error':'password or username or name must be at leat with 3 characters'}), 400 
        isUserExists = db.swcdb.user.isUserExists(user_id)
        if(isUserExists):
            return jsonify({'error':'user already exists'}), 400
        hashed_pwd = create_user_password_hash(request.json.pop('password'))
        user_created = db.swcdb.user.register_user(user_id,name, hashed_pwd)
        #token is an option instead 
        if(user_created):
            user_record = db.swcdb.user.get_user(user_id)
            login_user(User(user_id=user_record['user_id'], user_name=user_record['user_name'], password=user_record['hashed_pwd']))
            return jsonify({'ok': 'user created successfully', 'username': user_id}), 201
        else:
            return jsonify({'error':'something went wrong'}), 400
    except Exception as e:
        current_app.logger.error(f"Error: {e.__class__.__name__}: {str(e)}")  # This prints the type of the exception and the message
        return jsonify({'error': f'something went wrong: {e.__class__.__name__}'}), 400
    
@_app.route('/islogged')
def index():
    return "", (200 if current_user.is_authenticated else 401)

@_app.route('/user/delete/<user_id>', methods=["DELETE"])
@login_required
def delete_user(user_id):
    try: 
        res = db.swcdb.user.remove_user(user_id)
        if res: return "", 204
    except:
        return jsonify({'error':'something went wrong'}), 400

    
