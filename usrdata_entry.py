# This has the data that user enters in this file.
#seperate file to create functions that will enable the user to add data into the csv file. to keep the code cleaner.

from datetime import datetime

date_format = "%d-%m-%Y"
#created the variable to avoid the repetition of the date format
CATEGORIES = {"I": "Income", "E": "Expense"}
#created the dictionary to be able to add more categories in the future.

def get_date(prompt, allow_default=False):
    #initailly will asked to add the prompt. then if they press enter the default date will be passed.
    date_str = input(prompt)
    
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    # if the date string doesn't exist then return the default time in string format.
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Inavlid date format. Please enter the date in dd-mm-YYYY format")
        return get_date(prompt, allow_default)
    # a recursive function is being created where the function is recalled until we avoid getting Value error.

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        # value error as e is when the block of code raises an error it will store the error detils like invalid float literal. So the error details will be stored in e.
        print(e)
        return get_amount()

def get_category():
        category = input("Enter 'I' for Income or 'E' for Expense: ").upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
        return get_category()


def get_description():
    return input("Enter a descirption (optional): ")