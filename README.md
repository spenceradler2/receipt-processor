# Receipt Processor GO API

## Application Overview

This is a GO-based API that lets you process receipts and see how many points that receipt is worth based on a point system decribed by the readme in the https://github.com/fetch-rewards/receipt-processor-challenge/blob/main/README.md

The endpoints are /receipts/process and /receipts/{id}/points.
- The /receipts/process endpoint is POST that processes the receipt and calculates the points. 
- The /receipts/{id}/points endpoint is a GET that gets the points for the receipt with that id. 

## Requirements

Before running this application, make sure you have the following installed:
- [Go](https://golang.org/dl/) (version 1.18 or higher)
- [UUID Go library](https://pkg.go.dev/github.com/google/uuid) (included in the project as a dependency)

## Setup 

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone git@github.com:spenceradler2/receipt-processor.git
cd receipt-processor/
```
### Install Dependencies

Make sure the Go modules and dependencies are downloaded. This will be needed for github.com/google/uuid Run the below code:

```bash
go mod tidy
```

## Running the Application
Use the command below to run the application. You should see "Server is running on port 8080..." in the terminal.

```bash
go run main.go
```

## Testing
Once running the application can be tested by using curl or sending postman data to these endpoints. Sample data can be seen the original readme noted in the overview.

## Validations of receipts and ID   
Based on the API spec provided. Validations are included to validate if the data provided is in the correct format or has the information required.

## Testing for point calculator included
Included are commented out terminal logs for seeing the current point total after each rule is passed for testing and confirming the calculation is being done correct. 