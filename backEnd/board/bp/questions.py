from flask import   current_app ,jsonify, request, Blueprint
from flask_login import login_required, current_user
import db


_app = Blueprint('questions', __name__)
def init(app): app.register_blueprint(_app)

@_app.route('/questions', methods=["GET", "POST"])
@login_required
def questions():
    print(current_user.id)
    if(request.method == "POST"):
        try:
            db.swcdb.questions.add_questions()
            return jsonify({'ok':'questions are added'}), 201
        except:
            return jsonify({'error':'faild to adding the questions'}), 400
    else:
        questions = db.swcdb.questions.get_questions()
        return jsonify(questions), 200

    

    
