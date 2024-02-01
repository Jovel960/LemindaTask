from flask import  request, redirect, flash
from flask_login import login_required
import flask 
from db.swcdb.definer_columns import (QUESTIONS, USER, USER_FEEDBACK)


FEEDBKACk = {
    0: 'negative',
    1: 'positive'
}

feedBackOperations = flask.Blueprint("feedBackOperations", __name__)

feedBackOperations.route('')