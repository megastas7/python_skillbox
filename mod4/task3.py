import unittest
from task1 import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'
        self.data = {
            "email": "test@example.com",
            "phone": 9229999999,
            "name": "Maria",
            "address": "Ekaterinburg",
            "index": 1,
            "comment": "Hello"}

    def test_start_app(self):
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 200)

    def test_phone(self):
        self.data['phone'] = 'hello'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.data['phone'] = 99999999999999999999999999999999999999999
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_index(self):
        self.data['index'] = 'hello'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_index(self):
        self.data.pop('index', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_email(self):
        self.data['email'] = 'test'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.data['email'] = 1
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_email(self):
        self.data.pop('email', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_phone(self):
        self.data.pop('phone', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_address(self):
        self.data.pop('phone', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_name(self):
        self.data.pop('name', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)