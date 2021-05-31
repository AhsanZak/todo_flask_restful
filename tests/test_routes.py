from flask import Flask, request
import json
# from todo.routes import configure_routes
from todo.models import TodoSchema, Todo, todo_schema, todos_schema
import unittest
from run import app

def test_base_route():
    # app = Flask(__name__)
    # configure_routes(app)
    client = app.test_client()
    url='/'

    response = client.get(url)
    assert response.get_data() == b"<h2>This is home </h2>"
    assert response.status_code == 200


def test_post_route__success():
    # app = Flask(__name__)
    # configure_routes(app)
    client = app.test_client()
    url = '/todos'

    response = client.post(url, json={"title":"newe title", "status": "Not comopleted"})
    print(response)
    assert response.status_code == 200


#Check if Data returned
def test_todos_data():
    client = app.test_client()
    response = client.get("/todo")
    assert (b'title' in response.data)

#Check Content Type 
def test_get_todos_check_content_type_equals_json():
    client = app.test_client()
    response = client.get("/todo")
    assert response.content_type == 'application/json'
    assert response.status_code == 200

# Check each todo
def test_todo_by_id():
    client = app.test_client()
    url='/todo/{}'
    response = client.get(url.format(2))
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['title'] == 'This is the second Task to do'

#Check PUT todo
def test_put_todos():
    client = app.test_client()
    url='/todo/{}'
    response = client.put(url.format(1), json={"title":"Updatedd", "status": "completed"})
    assert response.status_code == 200


#Check DELETE todo
def test_put_todos():
    client = app.test_client()
    url='/todo/{}'
    response = client.delete(url.format(8))
    assert response.status_code == 200

#Check 404 errors
def test_404_routes():
    client = app.test_client()
    url='/hgjgkjasdfasdf'
    response = client.get(url)
    assert response.status_code == 200