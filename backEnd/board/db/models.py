from flask_login import UserMixin
import db

class User(UserMixin):
    def __init__(self, user_id, user_name, password):
        self.id=user_id
        self.username = user_name
        self.password = password
