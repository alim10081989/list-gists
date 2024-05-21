import unittest
from flask_testing import TestCase
from ..gists import app, GistsAPI

class TestGistsApp(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        self.github_api = GistsAPI()
        return app

    def test_index_route(self):
        """
        Test Main Welcome Page response and data
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Gists API", response.data)

    def test_gists_guide_route(self):
        """
        Test Gists Route Response and data
        """
        response = self.client.get('/gists/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username missing", response.data)

    def test_other_page_route(self):
        """
        Test route other than /gists route and return response
        """
        response = self.client.get('/unknown')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"The page named unknown does not exist", response.data)
    
    def test_verify_user_route(self):
        """
        Test validation of user
        """
        response = self.client.get("/gists/invalid_user")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User invalid_user does not exist", response.data)
    
    def test_search_gists(self):
        """
        Test results returned for mentioned user
        """
        gists = self.github_api.search_gists("octocat")
        self.assertIsInstance(gists, list)
    
    def test_unavailable_gists(self):
        """
        Test empty results returned for mentioned user
        """
        response = self.client.get("/gists/test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No public gists found for test", response.data)
    
    def test_check_response(self):
        """
        Test response returned 
        """
        response = self.github_api.check_response("https://api.github.com/users")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
