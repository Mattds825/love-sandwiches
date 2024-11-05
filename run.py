import gspread 
from google.oauth2.service_account import Credentials

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
    
# Accessing the sales worksheet
sales = SHEET.worksheet('sales')

# Accessing the data
data = sales.get_all_values()
print(data)