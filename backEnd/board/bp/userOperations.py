from flask import  request, Blueprint
from flask_login import login_required
from db.swcdb.definer_columns import (QUESTIONS, USER, USER_FEEDBACK)


FEEDBKACk = {
    0: 'negative',
    1: 'positive'
}

_app = Blueprint("feedBackOperations", __name__)
def init(app): app.register_blueprint(_app, url_prefix='/feedback')


@_app.route('/')
def index():
    return 'feedback'