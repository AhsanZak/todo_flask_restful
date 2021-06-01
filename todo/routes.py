from flask import request, jsonify, render_template, json, redirect, url_for
from todo import app, db
from todo.models import TodoSchema, Todo, todo_schema, todos_schema


# def configure_routes(app):
@app.route('/', methods=['GET', 'POST'])
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/create-todo', methods=['POST'])
def create_todo():
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        print("Title : ", title)

        new_todo = Todo(title, status)
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'result':'success', 'title':title, 'status': status})

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# API'S
# Create a Todo
@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    status = request.json['status']
    new_todo = Todo(title, status)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)

# Get all Todo's
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

    return todo_schema.jsonify(todo)
