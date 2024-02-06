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


@_app.route('/rate/<q_id>', methods=["PATCH"])
@login_required
def rate(q_id):
    is_qid_exists = db.swcdb.questions.verify_qid(q_id)
    if not is_qid_exists:
        return jsonify({'error':'q_id not exists'}), 400
    user_id=current_user.id
    rating = request.json.get("rating", None)
    if not (bool(rating) and rating in FEEDBKACK):
        return jsonify({"error":"rating is missing"}), 400
    print("asdasd", rating)
    res = db.swcdb.questions.user_op(q_id=q_id,user_id=user_id, rating=rating)
    if res:
        return jsonify(res), 200
    return jsonify({'error':'failed to update the user operation'}), 400

@_app.route('/comment/<q_id>', methods=["POST"])
@login_required
def add_feedback(q_id):
    is_qid_exists = db.swcdb.questions.verify_qid(q_id)
    if not is_qid_exists:
        return jsonify({'error':'q_id not exists'}), 400
    user_id=current_user.id
    feedback = request.json.get("feedback", None)
    if not bool(feedback):
        return jsonify({"error":"feedback is missing"}), 400
    res = db.swcdb.questions.user_op(q_id=q_id,user_id=user_id, feedback=feedback)
    if res:
        return jsonify(res), 200
    return jsonify({'error':'failed to update the user operation'}), 400

@_app.route('/comment/delete/<q_id>', methods=["POST"])
@login_required
def delete_feedback(q_id):
    is_qid_exists = db.swcdb.questions.verify_qid(q_id)
    if not is_qid_exists:
        return jsonify({'error':'q_id not exists'}), 400
    user_id=current_user.id
    res = db.swcdb.questions.delete_feedback(q_id,user_id)
    return jsonify(res), 200

#todo
@_app.route('/answer/<q_id>', methods=["POST"])
@login_required
def user_asnwer(q_id):
    is_qid_exists = db.swcdb.questions.verify_qid(q_id)
    if not is_qid_exists:
        return jsonify({'error':'q_id not exists'}), 400
    user_id = current_user.id
    user_ans = request.json.get("user_ans", None)
    if not bool(user_ans):
        return jsonify({'error':'user answer is missing'}), 400
    if not (user_ans in db.swcdb.questions.get_question_distractors(q_id)):
        return jsonify({'error':'user answer dosent match to the question distractors'}), 400
    res = db.swcdb.questions.user_op(q_id=q_id, user_id=user_id, user_ans=user_ans)
    if res:
        return jsonify(res), 200
    return jsonify({'error':'failed to update the user operation'}), 400
