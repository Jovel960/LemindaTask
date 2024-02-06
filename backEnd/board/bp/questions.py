from flask import   current_app ,jsonify, request, Blueprint
from flask_login import login_required, current_user
import db


_app = Blueprint('questions', __name__)
def init(app): app.register_blueprint(_app)

#for dev
@_app.route('/questions', methods=["GET", "POST"])
@login_required
def questions():
    if(request.method == "POST"):
            res = db.swcdb.questions.add_questions()
            if(res):
                 return jsonify(res), 201
            return jsonify({'error':'faild to adding the questions'}), 400
    else:
        questions = db.swcdb.questions.get_questions(current_user.id)
        if(questions):
            return jsonify(questions), 200
        return ({'error':'failed to fetch user questions'}), 400

    

    
