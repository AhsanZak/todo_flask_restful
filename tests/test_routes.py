from flask import Flask, request
import json
from todo.routes import configure_routes
from todo.models import TodoSchema, Todo, todo_schema, todos_schema

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url='/'

    response = client.get(url)
    assert response.get_data() == b"<h2>This is home </h2>"
    assert response.status_code == 200


# def test_post_route__success():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url = '/todos'
    
#     all_todos = Todo.query.all()
#     result = todos_schema.dump(all_todos)
    
#     mock_request_headers = {
#         'ContentType': 'application/json',
#         'dataType': 'json'
#     }

#     mock_request_data = result

#     response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
#     assert response.status_code == 200

# def test_get_todos_check_content_type_equals_json():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url='/todos'

#     response = client.get(url)
#     assert response.content_type == 'application/json'
#     assert response.status_code == 200


def test_todo_by_id():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url='/todo/{}'
    # For 200 Status
    response = client.get(url.format(test_todo_by_id))
    data = json.loads(response.data)
    assert response.status_code == HTTPStatus.OK
    # assert data['title']['status'] == ''