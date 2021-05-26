from flask import Flask
import json
from todo.routes import configure_routes

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url='/'

    response = client.get(url)
    assert response.get_data() == b"<h2>This is home </h2>"
    assert response.status_code == 200


# def test_post_todo_route():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url = '/todos'

#     request_headers = {
#         'Content-Type': 'application/json'
#     }

#     request_data = {
#         'request_id': 'application/json',
#         'payload': {
#             'py': 'pi',
#             'java': 'script'
#         }
#     }

#     response = client.post(url, data=json.dumps(request_data), headers=request_headers)
#     assert response.status_code == 200

