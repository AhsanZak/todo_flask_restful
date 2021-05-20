from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os
import json
import sqlite3

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.String(50))

    def __init__(self, title, status):
        self.title = title
        self.status = status

class TodoSchema(ma.Schema):
    class meta:
        fields = ('id', 'title', 'status')

# Init Schema 
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

@app.route("/todos", methods=["GET", "POST"])
def todos():
    if request.method == "GET":
        all_todos = Todo.query.all()
        result = todos_schema.dump(all_todos)
        return jsonify(result)

    if request.method == "POST":
        title = request.json['title']
        status = request.json['status']
        new_todo = Todo(title, status)
        db.session.add(new_todo)
        db.session.commit()
        return todo_schema.jsonify(new_todo)
        


@app.route("/todo/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_todo(id):
    if request.method == "GET":
        todo = Todo.query.get(id)
        return todo_schema.jsonify(todo)

    if request.method == "PUT":
        todo = Todo.query.get(id)

        title = request.json['title']
        status = request.json['status']

        todo.title = title
        todo.status = status
 
        db.session.commit()

        return todo_schema.jsonify(todo)

    if request.method == "DELETE":
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()

        return todo_schema.jsonify(todo)


if __name__ == "__main__":
    app.run(debug=True)