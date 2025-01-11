import unittest
import json
from app import app

#Creating unit tests to send receipts to the app and confirming the response is correct.
class ReceiptProcessorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a test client for Flask application.
        cls.client = app.test_client()

    def test_process_receipt_valid(self):
        # Test for valid receipt submission
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
            ],
            "total": "35.35"
        }

        response = self.client.post('/receipts/process', json=receipt_data)
        
        # Checks that the status code is 200.
        self.assertEqual(response.status_code, 200)
        
        # Checks that the response contains the receipt id.
        response_json = json.loads(response.data)
        self.assertIn('id', response_json)

    def test_process_receipt_invalid_retailer(self):
        # Test for invalid retailer format.
        receipt_data = {
            "retailer": "Target123^", # Invalid retailer.
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
            ],
            "total": "35.35"
        }
        
        response = self.client.post('/receipts/process', json=receipt_data)
        
        # Checks that the status code is 400.
        self.assertEqual(response.status_code, 400)
        
        # Checks for the correct error message in the response.
        response_json = json.loads(response.data)
        self.assertEqual(response_json['error'], 'The receipt is invalid')

    def test_process_receipt_invalid_date(self):
        # Tests for invalid date format.
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-35",  # Invalid date
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
            ],
            "total": "35.35"
        }
        
        response = self.client.post('/receipts/process', json=receipt_data)
        
        # Checks that the status code is 400.
        self.assertEqual(response.status_code, 400)
        
        # Checks for the correct error message in the response.
        response_json = json.loads(response.data)
        self.assertEqual(response_json['error'], 'The receipt is invalid')

    def test_get_points_valid(self):
    # Test for getting points of a valid receipt
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
            ],
            "total": "35.35"
        }

        # Posts receipt data.
        response = self.client.post('/receipts/process', json=receipt_data)
        receipt_id = json.loads(response.data)['id']

        # Gets points for the receipt.
        response = self.client.get(f'/receipts/{receipt_id}/points')
        
        # Checks that the status code is 200.
        self.assertEqual(response.status_code, 200)
        
        # Checks that the returned points for this is 28 per the example. 
        response_json = json.loads(response.data)
        self.assertEqual(response_json['points'], 28)


    def test_process_receipt_invalid_total(self):
        # Tests for invalid total format.
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
            ],
            "total": "35.35a"  # Invalid total
        }

        response = self.client.post('/receipts/process', json=receipt_data)

        # Checks that the status code is 400.
        self.assertEqual(response.status_code, 400)
        
        # Checks for the correct error message in the response.
        response_json = json.loads(response.data)
        self.assertEqual(response_json['error'], 'The receipt is invalid')

if __name__ == '__main__':
    unittest.main()