from flask import   current_app ,jsonify
from flask_login import login_required
import flask
import db


_app = flask.Blueprint('questions', __name__)
def init(app): app.register_blueprint(_app)

@_app.route('/questions', methods=["GET", "POST"])
@login_required
def set_questions():
    resFlag = db.swcdb.questions.add_questions()
    if resFlag:
        return jsonify({'ok':'questions are added'}), 201
    else:
        return jsonify({'error':'faild to adding the questions'}), 400
    
