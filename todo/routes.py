from flask import request, jsonify, render_template, json, redirect, url_for, abort, session
from todo import app, db, oauth, google
from todo.models import TodoSchema, Todo, todo_schema, todos_schema
from flask_login import current_user


# def configure_routes(app):
@app.route('/', methods=['GET', 'POST'])
def home():
    todo_list = Todo.query.all()
    email = dict(session).get('email', None)
    print(email)
    return render_template('index.html', todo_list=todo_list, email=email)


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    # do something with the token and profile
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/create-todo', methods=['POST', 'GET'])
def create_todo():
    if request.method == 'POST':
        new_title = request.form['title']
        new_status = request.form['status']

        #Check  if Todo Already exist or not
        if  Todo.query.filter_by(title=new_title).count() == 0:
            new_todo = Todo(new_title, new_status)
            db.session.add(new_todo)
            db.session.commit()
            print("New Todo Created")
            return jsonify({'result':'success', 'title':new_title, 'status': new_status})
        else:
            print("Error, Todo Already exist")
            return jsonify({'result':'error'})


@app.route('/update-todo', methods=['POST'])
def update():
    todo = Todo.query.filter_by(id=request.form['id']).first()
    todo.status = request.form['status']
    db.session.commit()
    return jsonify({'result':'success', 'status':todo.status})


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

    if  Todo.query.filter_by(title=title).count() == 0:
        new_todo = Todo(title, status)
        db.session.add(new_todo)
        db.session.commit()
        return todo_schema.jsonify(new_todo)
    else:
        print("Error, Todo Already exist")
        return jsonify({'result':'error'})


# Get all Todo's
@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

# Get Single Todo
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    if  Todo.query.filter_by(id=id).count() != 0:
        todo = Todo.query.get(id)
        return todo_schema.jsonify(todo)
    else:
        abort(400, description="Resource not found")

    
# Update a Todo
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    if  Todo.query.filter_by(id=id).count() != 0:
        todo = Todo.query.get(id)
        title = request.json['title']
        status = request.json['status']
        if  Todo.query.filter_by(title=title).count() == 0 or todo.title == title:
            todo.title = title
            todo.status = status
            db.session.commit()
            return todo_schema.jsonify(todo)
        else:
            return jsonify({'result':'Todo already exists with that title'})
    else:
        abort(400, description="Resource not found")

    

# Delete Todo
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    if  Todo.query.filter_by(id=id).count() != 0:
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()
        return ('', 204)
    else:
        abort(400, description="Resource not found")

    
