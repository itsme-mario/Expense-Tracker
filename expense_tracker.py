import argparse
import csv
import os
from datetime import datetime


parser = argparse.ArgumentParser(
                    prog='expense_tracker',
                    description='Program creates a csv of expenses and allows user to add, list, summarize, and delete expenses.',
                    epilog='Thank you for using the expense tracker program!')

parser.add_argument('operation', type=str, help='Operation to perform: add, list, summary, or delete')
parser.add_argument('-d', '--description', type=str, help='Description of the expense')
parser.add_argument('-a', '--amount', type=float, help='Amount of the expense')
parser.add_argument('-id', '--id', type=int, help='ID of the expense')
parser.add_argument('--month', type=int, help='Month for summary')

args = parser.parse_args()

file_name = "expenses.csv"

def add_expense(amount):
    prev_total = 0
    prev_ID = 0
    if os.path.exists(file_name):
        with open(file_name, 'r', newline='') as csvfile:
            expenses_reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')
            expenses_reader = csv.DictReader(csvfile)
            if expenses_reader:
                data = list(expenses_reader)
                if data:
                    prev_total = float(data[-1]['Total'])
                    prev_ID = int(data[-1]['ID'])

    with open('expenses.csv', 'a', newline='') as csvfile:
        expenses_writer = csv.DictWriter(csvfile, fieldnames=["ID", "Date", "Description", "Amount", "Total"])
        if sum(1 for line in open(file_name)) == 0:  # if file is empty, write header
            expenses_writer.writeheader()
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        expenses_writer.writerow({"ID": prev_ID + 1, "Date": current_datetime, "Description": args.description, "Amount": amount, "Total": prev_total + amount})

    return prev_ID + 1

def list_expenses():
    if os.path.exists(file_name):
        with open(file_name, 'r', newline='') as csvfile:
            expenses_reader = csv.DictReader(csvfile)
            data = list(expenses_reader)
            if not data:
                print("No expenses recorded yet.")
                exit()
            # Printing formatting
            cols = ["ID", "Date", "Description", "Amount", "Total"]
            widths = {
                col: max(
                    len(col),
                    *(len(str(row[col])) for row in data)
                )
                for col in cols
            }
            print(" ".join(f"{col:<{widths[col]}}" for col in cols))
            for row in data:
                if row['ID'] == 'ID':  # Skip header rows if they appear in the data
                    continue
                for col in cols:
                    if col == "Amount":
                        row[col] = f"${float(row[col]):.2f}"
                print(" ".join(f"{row[col]:<{widths[col]}}" for col in cols))
    else:
        print("No expenses recorded yet.")

def summary(month = None):
    monthsDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                  7: "July", 8: "August", 9: "September", 10: "October",
                  11: "November", 12: "December"}
    if os.path.exists(file_name):
        with open(file_name, 'r', newline='') as csvfile:
            expenses_reader = csv.DictReader(csvfile)
            data = list(expenses_reader)
            if not data:
                print("No expenses recorded yet.")
                exit()
            if month is not None:
                if month < 1 or month > 12:
                    print("Invalid month. Please enter a value between 1 and 12.")
                    return
                print(f"Total expenses for {monthsDict[month]}: ${sum(float(row['Amount']) for row in data if datetime.strptime(row['Date'], '%Y-%m-%d').month == month):.2f}")
            else:
                print(f"Total expenses: ${data[-1]['Total']}")
    else:
        print("No expenses recorded yet.")

def delete_expense(target_id):
    temp_file = "expenses_temp.csv"
    with open(file_name, newline='') as csvfile, open(temp_file, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        data = list(reader)
        deleted_amount = 0.0
        for row in data:
            if int(row['ID']) == target_id:
                deleted_amount = float(row['Amount'])
                break
        for row in data:
            if int(row['ID']) != target_id:  # keep rows that don't match target
                row['Total'] = str(float(row['Total']) - deleted_amount)
                if int(row['ID']) > target_id:
                    row['ID'] = str(int(row['ID']) - 1)
                writer.writerow(row)

    # Replace the original file with the filtered version
    os.replace(temp_file, file_name)

if args.operation == 'add':
    if args.description is None or args.amount is None:
        print("Description and amount are required for adding an expense.")
    else:
        print(f"Expense added successfully (ID: {add_expense(args.amount)})")

elif args.operation == 'list':
    list_expenses()

elif args.operation == 'summary':
    if args.month is not None:
        summary(args.month)
    else:
        summary()

elif args.operation == 'delete':
    if args.id is None:
        print("ID is required for deleting an expense.")
    elif args.id <= 0:
        print("ID must be a positive integer.")
    elif not os.path.exists(file_name):
        print("No expenses recorded yet.")
    elif args.id > sum(1 for line in open(file_name)) - 1:  # subtract 1 for header
        print("Expense with the given ID does not exist.")
    else:
        delete_expense(int(args.id))
        print(f"Expense deleted successfully.")