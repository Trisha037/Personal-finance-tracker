# this file the main flow of the program
import pandas as pd
#pandas allow us to load the csv file and work with it
import csv
from datetime import datetime
from usrdata_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

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

def plot_transactions(df):
    # takes the data frame as an argument and the data frame has all the transactions that needs to plotted.
    df.set_index('date', inplace=True)
    # index is the way to locate and manipulate different columns and sort by date to plot. Find the entires based on the date column.
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    # [df["category"] == "Income"] --> pick only rows with category Income
    # resample("D") --> D = daily; have dates of everyday.
    #sum() --> sum total income on each day.
    # renindex(df.index, fill_value=0) --> fill missing values with zero
    # returns the income df with category column set as Income, plot missing dates too within that graph in the frequency of dates.
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    # create a plot figure the size of the screen where the plot is and the size is 10 by 5
    plt.plot(income_df.index,income_df["amount"], label="Income", color='g')
    # plotting the date index and the amount column label the plot line as income and the plot line will be green.
    plt.plot(expense_df.index,expense_df["amount"], label="Expense", color='r')
    # plotting the date index and the amount column label the plot line as expense and the plot line will be red.
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expense Over Time')
    plt.legend() # see the labels of the different plots
    plt.grid(True) # see the grid to see the plots
    plt.show() # will show the graph
    

def main():
    #This function is created to make it more interactive instead of calling all the other methods and functions.
    while True:
        print("\n1. Add a new transaction.")
        print("2. View transactions and summary within a given range date.")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date,end_date)
            if  input("Do you want see the plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting..")
            break
        else:
            print("Invalid choice. Enter 1,2, or 3")

if __name__ == "__main__":
    #the main function wil only run if the main file runs itself. if main file initiated by something else it will not run.
    main()

            

