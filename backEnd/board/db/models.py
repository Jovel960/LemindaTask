from flask_login import UserMixin
import db

class User(UserMixin):
    def __init__(self, user_id, user_name, password):
        self.id=user_id
        self.username = user_name
        self.password = password

    @staticmethod
    def get(user_name):
        user = db.swcdb.user.get_user(user_name)
        return user

    def get_id(self):
        return str(self.id) #in case