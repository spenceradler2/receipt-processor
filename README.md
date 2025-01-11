# Receipt Processor GO or Python with Flask API

## Application Overview

(Since the preferred language was GO and to show I could learn and implement a GO application I created a GO server to be run. I was then informed it is not a strong preference for GO and I would be asked questions where I would have to manipulate the code during the interview and since I just learned GO for this challenge I thought it would make sense to have a Python with Flask server that I am much more familar with. I included requirements to run both in my readme)

This is a GO-based or Python with Flask API that lets you process receipts and see how many points that receipt is worth based on a point system decribed by the readme in the https://github.com/fetch-rewards/receipt-processor-challenge/blob/main/README.md

The endpoints are /receipts/process and /receipts/{id}/points.
- The /receipts/process endpoint is POST that processes the receipt and calculates the points. 
- The /receipts/{id}/points endpoint is a GET that gets the points for the receipt with that id. 

## Requirements

Before running this application, make sure you have the following installed:

For GO:
- [Go](https://golang.org/dl/) (version 1.18 or higher)
- [UUID Go library](https://pkg.go.dev/github.com/google/uuid) (included in the project as a dependency)

For Python with GO:
Refer to the dockerfile to run the requirements.txt file
## Setup 

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone git@github.com:spenceradler2/receipt-processor.git
cd receipt-processor/
```
### Install Dependencies For GO (Not Required for Python with Flask)

Make sure the Go modules and dependencies are downloaded. This will be needed for github.com/google/uuid Run the below code:

```bash
go mod tidy
```

## Running the Application

Use the command below to run the application. You should see "Server is running on port 8080..." in the terminal.

For GO:
```bash
go run go/main.go
```
For Python with Flask:
Refer to the dockerfile.

## Testing
Once running the application can be tested by using curl or sending postman data to these endpoints. Sample data can be seen the original readme noted in the overview. Additionally for the Python with Flask application unit tests were set up to send some sample receipts to the app to confirm some of the formats and responses are working correctly. The unit tests can be run by CDing into the python with flask folder and running python -m unittest test_app.py

## Validations of receipts and ID   
Based on the API spec provided. Validations are included to validate if the data provided is in the correct format or has the information required.

## Testing for point calculator included
Included are commented out terminal logs for seeing the current point total after each rule is passed for testing and confirming the calculation is being done correct. 