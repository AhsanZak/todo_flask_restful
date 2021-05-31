from flask import request, jsonify
from todo import app, db
from todo.models import TodoSchema, Todo, todo_schema, todos_schema


# def configure_routes(app):
@app.route('/')
def home():
    return "<h2>This is home </h2>"
# Create a Product
@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    status = request.json['status']
    new_todo = Todo(title, status)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)

@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

# Get Single Todo
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)

# Update a Todo
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    title = request.json['title']
    status = request.json['status']

    todo.title = title
    todo.status = status
    db.session.commit()
    return todo_schema.jsonify(todo)

# Delete Todo
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()

<<<<<<< HEAD
    return todo_schema.jsonify(todo)
=======
    return todo_schema.jsonify(todo)
>>>>>>> unitest
