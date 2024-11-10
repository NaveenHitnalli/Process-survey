import sys
import os
import unittest
from sanic import Sanic
from sanic_testing import TestManager
from sanic.response import json as sanic_json

# Add the directory containing 'sanicapp.py' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sanicapp import app  # Import the Sanic app

class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.app = TestManager(app)

    def test_process_survey(self):
        test_data = {
            "user_id": "test_user",
            "survey_results": [
                {"question_value": 1},
                {"question_value": 2},
                {"question_value": 3},
                {"question_value": 4},
                {"question_value": 5},
                {"question_value": 6},
                {"question_value": 7},
                {"question_value": 8},
                {"question_value": 9},
                {"question_value": 10},
                {"question_value": 5}  
            ]
        }
        request, response = self.app.test_client.post("/process-survey", json=test_data)
        self.assertEqual(response.status, 200)
        self.assertIn("overall_analysis", response.json)

if __name__ == "__main__":
    unittest.main()
