from unittest import TestCase
from server import app
from flask import session
from model import connect_to_db,Todo,Todo_item
class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app,echo=False)

    def test_register_user(self):
        """Test if user can be registered successfully"""

        response = self.client.post("/users",
                                    data={"email": "test@test.com",
                                          "password": "password123"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/login")

    def test_login(self):
        """Test that a user can log in successfully"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = "test@test.com"
        response = self.client.post("/todos",
                                    data={"email": "test@test.com",
                                          "password": "test"},
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome! test@test.com!", response.data)
        self.assertEqual(sess["user_email"], "test@test.com")

    def test_invalid_login(self):
        """Test that an invalid login attempt fails"""

        response = self.client.post("/todos",
                                    data={"email": "test@test.com",
                                          "password": "invalidpassword"},
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The email or password you entered was incorrect.", response.data)

    def test_detail_route_for_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = "test@test.com"
        response = self.client.get('/todos')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Actions', response.data)

    def test_create_list_route(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = "test@test.com"
        response = self.client.post("/create/",
                                    data={
                                        "description" : "test1",
                                        "notes" : "test1",
                                        "category" : "Work",
                                    },follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'test1',response.data)
        self.assertIn(b'test1',response.data)
        self.assertIn(b'Work',response.data)

    def test_show_todo_detail(self):
        todo_list_id = 14
        response = self.client.get(f"/todos/{todo_list_id}")
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Completed', response.data)

    def test_logout(self):
        response = self.client.get("/logout",follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'you have successfully logout',response.data)

    def test_pexels_api(self):
        response =self.client.get('/api/pexels/baby')
        self.assertEqual(response.status_code,200)
        data = response.json
        self.assertTrue('photos' in data)
        self.assertTrue(len(data['photos']) == 4)








if __name__ == '__main__':
    import unittest
    print("\\\\\\\\\\\\starttest")
    unittest.main()
