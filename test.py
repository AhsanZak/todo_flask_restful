import requests

try:
    from run import app
    import unittest
except Exception as e:
    print("Something is not right {} ".format(e))


def test_post_route__success():
    client = app.test_client()
    url = '/todos'

    response = client.post(url, json={'title': 'new title', 'status': 'Not COmpelted'})
    print(response)
    assert response.status_code == 200



class FlaskTest(unittest.TestCase):

    # Check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #Check if content return is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/todo")
        self.assertEqual(response.content_type, "application/json")

    #Check if Data returned
    def test_todos_data(self):
        tester = app.test_client(self)
        response = tester.get("/todo")
        self.assertTrue(b'title' in response.data)

        
    def test_post_route__success(self):
        tester = app.test_client(self)
        url = '/todos'

        response = tester.post(url, json={'title': 'new 2nd title', 'status': 'Nott COmpelted'})
        print(response)
        self.assertEqual(response.status_code, 200)

    # #Check POST to todos
    # API_URL = "http://127.0.0.1:5000"
    # TODOS_URL = "{}/todos".format(API_URL)
    # TODOS_OBJ = {
    #     "id": 3,
    #     "status": "Not yet Completed",
    #     "title": "This is theasdjkfahsfahsk to do"
    # }
    # def test_todos_post(self):
    #     response = requests.post(FlaskTest.TODOS_URL, json=FlaskTest.TODOS_OBJ)
    #     self.assertEqual(response.status_code, 201)

    # def test_get_todo(self):
    #     id=4
    #     r = requests.get("{}/{}".format(FlaskTest.TODOS_URL, id))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertDictEqual(r.json(), FlaskTest.TODOS_OBJ)


if __name__ == "__main__":
    unittest.main()
