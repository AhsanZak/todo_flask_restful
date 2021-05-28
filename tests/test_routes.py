from flask import Flask, request
import json
from todo.routes import configure_routes
from todo.models import TodoSchema, Todo, todo_schema, todos_schema
import unittest

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url='/'

    response = client.get(url)
    assert response.get_data() == b"<h2>This is home </h2>"
    assert response.status_code == 200


def test_post_route__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/todos'

    data = {"title":"testing todo", "status":"Noy completed"}

    response = client.post(url, data)
    assert response.status_code == 200


#Check if Data returned
def test_todos_data(self):
    tester = app.test_client(self)
    response = tester.get("/todo")
    self.assertTrue(b'title' in response.data)

# def test_get_todos_check_content_type_equals_json():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url='/todos'

#     response = client.get(url)
#     assert response.content_type == 'application/json'
#     assert response.status_code == 200


# def test_todo_by_id():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url='/todo/{}'
#     # For 200 Status
#     response = client.get(url.format(test_todo_by_id))
#     data = json.loads(response.data)
#     assert response.status_code == HTTPStatus.OK
#     # assert data['title']['status'] == ''



