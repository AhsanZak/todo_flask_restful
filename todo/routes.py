from flask import request, jsonify, render_template, json, redirect, url_for, abort, session, flash, redirect
from todo import app, db, oauth, google, bcrypt
from todo.models import TodoSchema, Todo, todo_schema, todos_schema, User
from flask_login import current_user, login_user, logout_user, login_required
from todo.forms import RegistrationForm, LoginForm



# def configure_routes(app):
@app.route('/', methods=['GET', 'POST'])
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
    return render_template('login.html', form=form)  

@app.route('/google-login')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    if User.query.filter_by(email=user_info.get('email')).count() == 0:
        user = User(username=user.get('name'), email=user.get('email'), password="$#$#$#$2#$@")
        db.session.add(user)
        db.session.commit()
        
    user = User.query.filter_by(email=user_info.get('email')).first()
    login_user(user)
    return redirect('/')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create-todo', methods=['POST', 'GET'])
def create_todo():
    if current_user.is_authenticated:
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
                error = "Todo Already exists"
                return jsonify({'result':error})
    else:
        print("Not authenticated")
        error = "Please login to Add Todo"
        return jsonify({'result':error})



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

    
