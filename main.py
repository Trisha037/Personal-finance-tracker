# this file the main flow of the program
import pandas as pd
#pandas allow us to load the csv file and work with it
import csv
from datetime import datetime
from usrdata_entry import get_amount, get_category, get_date, get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    # class variable as it is associated with the class. it holds the csv file.
    COLUMNS = ["date", "amount", "category", "description"]
    # class variables which introduces the fieldnames of the columns in the CSV file. Which is made global.
    FORMAT = "%d-%m-%Y"
    

    #initialise the csv file. read it if it already exists or create it if it doesn't exist.

    @classmethod #this is class method decorator for the initialiser.
    # class method will take the entire class 'cls' as the object not 'self'
    #This is class method will not have access to the object of the class (as it have other extra functions and properties in addition to the class defined). But can have access to the class defined variables and functions.
    def initialise_csv(cls):
        # takes parameter cls
        try:
            pd.read_csv(cls.CSV_FILE)
            #reads the existing finance data csv file if it exists
        except FileNotFoundError:
            df  = pd.DataFrame(columns= cls.COLUMNS)
            #if the file doesn't exist yet create the file using the data frame data structure (2-D data structure that holds a 2-D array or a table with rows an columns). data frame also access to columns and rowas from a csv file.
            df.to_csv(cls.CSV_FILE, index=False)
            #data frame will be xported to a csv file in the same directory as a local file as this python file. do not sort by index.
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        #creating a data entry method to add the data into the CSV file
        new_entry = {
            "date": date,
            "amount": amount,
            "category":category,
            "description": description
        }
        # created a python dictionary so that the entered data will go into the correct column when the CSV_writer is used. it is another pandas function.
        with open (cls.CSV_FILE, "a", newline="") as csvfile:
            # open CSV file in "a"-append mode and do not add a new line.
            # with open line is context manager - where the open file is stored in the variable "csvfile". when the code below it is taken care of, the file will close itself. after making the necessary changes.
            #best practise to use the with open.
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            # creating a CSV writer object, which takes dictionary and writes it into the CSV file.
            writer.writerow(new_entry)
            #create a new row with the new entry.
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        #a method to return all the transactions within given dates.
        df = pd.read_csv(cls.CSV_FILE)
        #"cls.CSV_FILE" where cls is the object and CSV_FILE is the file path of that object.
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        # data frame will take the "date" column and using pandas method will convert all the dates in the column into "%d-%m-%Y" format
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        # the start time which will be taken as the parameter will be taken as a string which will then e converted into a similar format as above.
        end_date = datetime.strptime(end_date,CSV.FORMAT)
        #same thing is done with end time
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        # mask is technique used for data frames when checking and filter every row within a specific column. '&' is called a bitwise operator and it is used specifically for masks and dataframes.
        # mask meths is an application of the if-then idiom. rplaces the values of the rows where the condition evaluated to True.
        filtered_df = df.loc[mask]
        # loc method will access a group of rows and columns within the dataframe and apply the mask condition.

        if filtered_df.empty:
            print('No transactions found in the given date range.')
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            # This is like a heading.
            #next will print all the filtered data frames 
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            #the lambda function will take x as the parameter and applies the format. where x is the date.


            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            #using the filteref data frame to filter the categories by Income and Expense and take the amount within them and sum them individually.

            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Total Expense: ${(total_income-total_expense):.2f}")

        return filtered_df


def add():
    #defining the function to initialise the addition of the following columns
    CSV.initialise_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

CSV.get_transactions("01-01-2023","01-01-2025")
add()

            

