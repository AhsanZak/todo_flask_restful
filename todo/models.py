from todo import db, ma, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50))

    def __init__(self, title, status):
        self.title = title
        self.status = status

# todo Schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'status')

# Init schema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
