from flask import  request, Blueprint, jsonify
from flask_login import login_required, current_user
from db.swcdb.definer_columns import (QUESTIONS, USER, USER_FEEDBACK)
import db


FEEDBKACK = {
    "0": 'negative',
    "1": 'positive'
}

_app = Blueprint("feedBackOperations", __name__)
def init(app): app.register_blueprint(_app, url_prefix='/feedback')


@_app.route('/rate/<q_id>', methods=["POST"])
@login_required
def rate(q_id):
    user_id=current_user.id
    rating = request.json["rating"].strip()
    if not bool(rating):
        return jsonify({"error":"rating is missing"}), 401
    db.swcdb.questions.rating(q_id,user_id, FEEDBKACK[rating])
    return 'ok'

@_app.route('/<q_id>', methods=["POST"])
@login_required
def feedback(q_id):
    user_id=current_user.id
    feedback = request.json["feedback"]
    if not bool(feedback):
        return jsonify({"error":"feedback is missing"}), 400
    # db.swcdb.questions.feeedback(q_id,user_id, "hello", FEEDBKACk["1"])
    return 'ok'