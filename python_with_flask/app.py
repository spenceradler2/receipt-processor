#Importing required packages
import uuid
import math
import re
from datetime import datetime
from flask import Flask, request, jsonify

# Initializing the Flask app
app = Flask(__name__)

# In-memory store for receipts
receipt_store = {}

# Creating the class
class Receipt:
    def __init__(self, retailer, purchase_date, purchase_time, items, total):
        self.id = str(uuid.uuid4()) #Creating a unique ID for the receipt using uuid
        self.retailer = retailer
        self.purchase_date = purchase_date
        self.purchase_time = purchase_time
        self.items = items
        self.total = total
        self.calculated_points = self.calculate_points() #Calcuating points 

    #Creating a fuction to calculate the points of the receipt. 
    def calculate_points(self):
        #Setting intial value of points to 0
        points = 0
        total = parse_total(self.total)

        # One point for every alphanumeric character in the retailer name.
        points += count_alphanumeric(self.retailer)
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Alphanumeric: {points}")
        
        # 50 points if the total is a round dollar amount (no cents)
        if total == int(total):
            points += 50
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Total round: {points}")

        # 25 points if total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Mutiple 25: {points}")
        
        # 5 points for every two items in the receipt
        points += (len(self.items) // 2) * 5
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"2 items: {points}")

        # If description length of any item is multiple of 3, calculate points
        for item in self.items:
            if len(item['shortDescription'].strip()) % 3 == 0:
                price = parse_total(item['price'])
                points += math.ceil(price * 0.2)
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Trimmed length: {points}")
        
        # 6 points if the day of purchase date is odd
        purchase_date = datetime.strptime(self.purchase_date, "%Y-%m-%d")
        if purchase_date.day % 2 != 0:
            points += 6
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Purchase Day: {points}")

        
        # 10 points if the purchase time is between 2:00pm and 4:00pm
        purchase_time = datetime.strptime(self.purchase_time, "%H:%M")
        if 14 < purchase_time.hour < 16 or (purchase_time.hour == 14 and purchase_time.minute >= 1):
            points += 10
        #Below is for testing a part of the calculated points to see if there are any issues
        # print(f"Purchase Time: {points}")
            
        return points
    
# Helper function to parse the total into a float to run calculations on.
def parse_total(total):
    try:
        return float(total)
    except ValueError:
        return 0.0

# Helper function to count alphanumeric characters
def count_alphanumeric(s):
    return sum(1 for ch in s if ch.isalnum())
# Helper function to confirm retailer is in the correct format
def is_valid_retailer(retailer):
    return bool(re.match(r"^[\w\s\-\&]+$", retailer))
# Helper function to confirm total is in the correct format
def is_valid_total(total):
    return bool(re.match(r"^\d+\.\d{2}$", total))
# Helper function to confirm item description is in the correct format
def is_valid_item_description(description):
    return bool(re.match(r"^[\w\s\-]+$", description))
# Helper function to confirm price is in the correct format
def is_valid_price(price):
    return bool(re.match(r"^\d+\.\d{2}$", price))

# Function to validate if the receipt is valid by checking all required validations from the API
def validate_receipt(receipt):
    # Validates retailer format using helper function
    if not is_valid_retailer(receipt['retailer']):
        return "Invalid retailer"
    # Validates purchase date format
    try:
        datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
    except ValueError:
        return "Invalid purchase date"
    # Validates purchase time format
    try:
        datetime.strptime(receipt['purchaseTime'], "%H:%M")
    except ValueError:
        return "Invalid purchase time"
    # Validates total using helper function
    if not is_valid_total(receipt['total']):
        return "Invalid total"
    # Validates number of items
    if len(receipt['items']) < 1:
        return "Minimum number of items not met"
    # Loop through all items
    for item in receipt['items']:
        # Validates Item Description using helper function
        if not is_valid_item_description(item['shortDescription']):
            return "Invalid item description"
        # Validates Price using helper function
        if not is_valid_price(item['price']):
            return "Invalid item price"
    # If no issues return None
    return None

# Routes
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.get_json()
    
    # Validations for receipt requirements listed in API
    validation_error = validate_receipt(receipt_data)
    if validation_error:
        return jsonify({'error': 'The receipt is invalid'}), 400

    # Create Receipt object
    receipt = Receipt(
        retailer=receipt_data['retailer'],
        purchase_date=receipt_data['purchaseDate'],
        purchase_time=receipt_data['purchaseTime'],
        items=receipt_data['items'],
        total=receipt_data['total']
    )

    # Store the with that id in memory to be checked later
    receipt_store[receipt.id] = receipt
    # Response with required information from API the receipt ID
    return jsonify({'id': receipt.id}), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    # Getting the ID from the given path and confirming it is in the store to confirm it is valid
    receipt = receipt_store.get(receipt_id)
    if not receipt:
        return jsonify({'error': 'No receipt found for that ID'}), 400
    # Calculated points response
    return jsonify({'points': receipt.calculated_points}), 200

if __name__ == '__main__':
    app.run(port=8080)
    print("Server is running on port 8080...")