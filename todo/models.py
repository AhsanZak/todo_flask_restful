from todo import db, ma

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