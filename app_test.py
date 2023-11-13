import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_recipes(self):
        response = self.app.get('/recipes')
        self.assertEqual(response.status_code, 200)

    def test_search_recipes(self):
        response = self.app.get('/search?term=pasta')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
