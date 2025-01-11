package main

//Importing required packages
import (
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"
	"unicode"

	"github.com/google/uuid"
)

// Creating data structures for the json data
type Receipt struct {
	ID               string `json:"id,omitempty"`
	Retailer         string `json:"retailer"`
	PurchaseDate     string `json:"purchaseDate"`
	PurchaseTime     string `json:"purchaseTime"`
	Items            []Item `json:"items"`
	Total            string `json:"total"`
	CalculatedPoints int    `json:"calculatedPoints,omitempty"`
}

type Item struct {
	ShortDescription string `json:"shortDescription"`
	Price            string `json:"price"`
}

// Storing the receipts in an in memory map
var receiptStore = make(map[string]Receipt)

func main() {
	//HTTP Handlers for required routes
	http.HandleFunc("/receipts/process", processReceipt)
	http.HandleFunc("/receipts/", getPoints)

	//Console log that the server is running
	fmt.Println("Server is running on port 8080...")
	http.ListenAndServe(":8080", nil)
}

func processReceipt(w http.ResponseWriter, r *http.Request) {
	var receipt Receipt
	err := json.NewDecoder(r.Body).Decode(&receipt)
	// If the request has an issue getting through and being parsed
	if err != nil {
		http.Error(w, "The receipt is invalid", http.StatusBadRequest)
		return
	}
	//Validations for receipt requirements listed in API
	if err := validateReceipt(receipt); err != nil {
		http.Error(w, "The receipt is invalid", http.StatusBadRequest)
		return
	}
	//Creating a unique ID for the receipt using uuid
	receipt.ID = uuid.New().String()

	//Calculating the points for the receipts
	receipt.CalculatedPoints = calculatePoints(receipt)

	//Store the with that id in memory to be checked later
	receiptStore[receipt.ID] = receipt

	//Response with required information from API the receipt ID
	response := map[string]string{"id": receipt.ID}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func getPoints(w http.ResponseWriter, r *http.Request) {
	//Getting the ID from the given path and confirming it is in the store to confirm it is valid
	id := r.URL.Path[len("/receipts/") : len(r.URL.Path)-7]
	receipt, found := receiptStore[id]
	if !found {
		http.Error(w, "No receipt found for that id", http.StatusBadRequest)
		return
	}
	//Calculated points response
	response := map[string]int64{"points": int64(receipt.CalculatedPoints)}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// Function to validate if the receipt is valid by checking all required validations from the API
func validateReceipt(receipt Receipt) error {
	//Validates retailer format using helper function
	if !isValidRetailer(receipt.Retailer) {
		return errors.New("invalid retailer")
	}
	//Validates purchase date format
	if _, err := time.Parse("2006-01-02", receipt.PurchaseDate); err != nil {
		return errors.New("invalid purchase date")
	}
	//Validates purchase time format
	if _, err := time.Parse("15:04", receipt.PurchaseTime); err != nil {
		return errors.New("invalid purchase time")
	}
	//Validates total using helper function
	if !isValidTotal(receipt.Total) {
		return errors.New("invalid total")
	}
	//Validates number of items
	if len(receipt.Items) < 1 {
		return errors.New("minimim number of items not met")
	}
	//Loop through all items
	for _, item := range receipt.Items {
		//Validates Item Description using helper function
		if !isValidItemDescription(item.ShortDescription) {
			return errors.New("invalid description")
		}
		//Validates Price using helper function
		if !isValidPrice(item.Price) {
			return errors.New("invalid price")
		}
	}
	//If no issues return nil
	return nil
}

// Helper function to confirm retailer is in the correct format
func isValidRetailer(retailer string) bool {
	match, _ := regexp.MatchString("^[\\w\\s\\-&]+$", retailer)
	return match
}

// Helper function to confirm total is in the correct format
func isValidTotal(total string) bool {
	match, _ := regexp.MatchString("^\\d+\\.\\d{2}$", total)
	return match
}

// Helper function to confirm item description is in the correct format
func isValidItemDescription(description string) bool {
	match, _ := regexp.MatchString("^[\\w\\s\\-]+$", description)
	return match
}

// Helper function to confirm price is in the correct format
func isValidPrice(price string) bool {
	match, _ := regexp.MatchString("^\\d+\\.\\d{2}$", price)
	return match
}

// Function to calculate points of the receipt based on rules in Readme
func calculatePoints(receipt Receipt) int {
	//Setting intial value of points to 0
	points := 0
	//Handling errors of parsing total from string to float
	total, err := parseTotal(receipt.Total)
	if err != nil {
		return points
	}

	//One point for every alphanumeric character in the retailer name.
	points += countAlphanumeric(receipt.Retailer)
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Alphanumeric:", points)

	//50 points if the total is a round dollar amount with no cents.
	if total == float64(int(total)) {
		points += 50
	}
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Total round:", points)

	//25 points if the total is a multiple of 0.25.
	if math.Mod(total, .25) == 0 {
		points += 25
	}
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Multiple 25:", points)

	//5 points for every two items on the receipt.
	points += (len(receipt.Items) / 2) * 5
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("2 items:", points)

	//If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
	for _, item := range receipt.Items {
		if len(strings.TrimSpace(item.ShortDescription))%3 == 0 {
			price, _ := parseTotal(item.Price)
			points += int(math.Ceil(price * .2))
		}
	}
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Trimmed length:", points)

	//6 points if the day in the purchase date is odd.
	purchaseDate, _ := time.Parse("2006-01-02", receipt.PurchaseDate)
	if purchaseDate.Day()%2 != 0 {
		points += 6
	}
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Purchase Day:", points)

	//10 points if the time of purchase is after 2:00pm and before 4:00pm.
	purchaseTime, _ := time.Parse("15:04", receipt.PurchaseTime)
	if purchaseTime.Hour() > 14 || (purchaseTime.Hour() == 14 && purchaseTime.Minute() >= 1) && purchaseTime.Hour() < 16 {
		points += 10
	}
	//Below is for testing a part of the calculated points to see if there are any issues
	// fmt.Println("Purchase Time:", points)

	return points
}

// Helper function to parse the total into a float to run calculations on
func parseTotal(total string) (float64, error) {
	return strconv.ParseFloat(total, 64)
}

// Helper function to count alphanumeric characters
func countAlphanumeric(s string) int {
	count := 0
	for _, ch := range s {
		//Sometimes some special characters are considered alphanumeric. This can be adjusted as needed based on reviews understanding. For now was assuming just letters and numbers but can add some special characters.
		if unicode.IsLetter(ch) || unicode.IsDigit(ch) {
			count++
		}
	}
	return count
}
