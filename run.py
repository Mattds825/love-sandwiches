import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# Defining the scope
# lists the APIs that the program should access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",  # Corrected URL
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Getting the credentials
CREDS = Credentials.from_service_account_file('creds.json')

# Creating a client
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Accessing the Google Sheet
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user    
    """
    while True:    
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60 \n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        
        # validate the data, break the loop if valid
        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data
        
def validate_data(values):
    """
    Inside the try convert all string values into integers.
    Raise ValueError if strings cannot be converted into int,
    or if there are not exactly 6 values.
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False
    return True


def update_sales_worksheet(data):
    """
    Update the sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    
    # Access the sales worksheet
    # Append the data provided
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data) 
    
    print("Sales worksheet updated successfully.\n")
    
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure subtracted from the stock:
        - Positive surplus indicates waste
        - Negative surplus indicates stock was made after sold out
    """
    print("Calculating surplus data...\n")
    
    stock = SHEET.worksheet('stock').get_all_values()
    
    # get the last row of stock data, convert to integers
    stock_row = [int(s) for s in stock[-1]]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    
    return surplus_data

def update_surplus_worksheet(data):
    """
    Update the surplus worksheet, add new row with the list data provided
    """
    print("Updating surplus worksheet...\n")
    
    # Access the surplus worksheet
    # Append the data provided
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data) 
    
    print("Surplus worksheet updated successfully.\n")

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print("Welcome to Love Sandwiches Data Automation")
main()
