# test_client.py
import unittest
from unittest.mock import patch, MagicMock
from geocode_utils import ping

class TestClient(unittest.TestCase):
    def setUp(self):
        self.url = "https://google.com"

    @patch("geocode_utils.requests")
    def test_ping_returns_200(self, mock_requests):
        # mock a 200 response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        result = ping(self.url)
        self.assertTrue(result)
    
    @patch("geocode_utils.requests")
    def test_ping_returns_500(self, mock_requests):
        # mock a 500 response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests.get.return_value = mock_response

        result = ping(self.url)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
