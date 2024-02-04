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
    if not (bool(rating) and rating in FEEDBKACK):
        return jsonify({"error":"rating is missing"}), 400
    res = db.swcdb.questions.rating(q_id,user_id, rating)
    return jsonify(res), 200

@_app.route('/comment/<q_id>', methods=["POST"])
@login_required
def feedback(q_id):
    user_id=current_user.id
    feedback = request.json["feedback"]
    if not bool(feedback):
        return jsonify({"error":"feedback is missing"}), 400
    res = db.swcdb.questions.feedback(q_id,user_id, "hello")
    return jsonify(res), 200
