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

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    
    print(f"Updating {worksheet} worksheet...\n")
    
    # Access the worksheet
    # Append the data provided
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data) 
    
    print(f"{worksheet} worksheet updated successfully.\n")
    

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches Data Automation")
main()
