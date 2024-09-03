import unittest
import sys
from unittest.mock import patch, MagicMock
from flask import Flask

sys.path.append('../src')

from app import app, get_lat_lon_from_city_state, get_lat_lon_from_zip


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.requests.get')
    def test_get_lat_lon_from_city_state_success(self, mock_get):
        # Mock the API response
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "geometry": {
                    "location": {
                        "lat": 40.712776,
                        "lng": -74.005974
                    }
                }
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the function
        lat, lng = get_lat_lon_from_city_state("New York", "NY")

        # Assertions to check if the function returns the correct coordinates
        self.assertEqual(lat, 40.712776)
        self.assertEqual(lng, -74.005974)

    @patch('app.requests.get')
    def test_get_lat_lon_from_city_state_failure(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        lat, lng = get_lat_lon_from_city_state("Unknown Location", "Unknown State")
        self.assertIsNone(lat)
        self.assertIsNone(lng)

    @patch('app.requests.get')
    def test_successful_geocode_Zipcode(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "geometry": {
                    "location": {"lat": 34.0522, "lng": -118.2437}
                },
                "address_components": [
                    {"types": ["locality"], "long_name": "Los Angeles"},
                    {"types": ["administrative_area_level_1"], "short_name": "CA"}
                ]
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Execute
        lat, lng, city, state = get_lat_lon_from_zip("90001")

        # Assert
        self.assertEqual(lat, 34.0522)
        self.assertEqual(lng, -118.2437)
        self.assertEqual(city, "Los Angeles")
        self.assertEqual(state, "CA")

    @patch('app.requests.get')
    def test_api_failure_Zipcode(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Execute
        result = get_lat_lon_from_zip("99999")

        # Assert
        self.assertEqual(result, (None, None, None, None))


if __name__ == '__main__':
    unittest.main()
