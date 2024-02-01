from flask import   current_app ,jsonify, request
from flask_login import login_required, current_user
import flask
import db


app_questions = flask.Blueprint('questions', __name__)

@app_questions.route('/questions', methods=["GET", "POST"])
@login_required
def set_questions():
    resFlag = db.swcdb.questions.add_questions()
    if resFlag:
        return jsonify({'ok':'questions are added'}), 201
    else:
        return jsonify({'eror':'faild to adding the questions'})
    
