from models.Database import Database
import sqlite3
from datetime import timedelta
from datetime import datetime
import calendar

db = Database()

def average_expenses(time='all'):
        try:
            # Generate entries based on delay.
            query = 'SELECT Date , Amount FROM transaction_history WHERE Amount < 0 AND Date > ? ;'
            if time == 'all':
                delay = 0
            elif time == 'day':
                delay = 1
            elif time == 'week':
                delay = 7
            elif time == 'month':
                delay = 31
            elif time == 'year':
                delay = 365
            choice = str((datetime.now() - timedelta(days=delay)).strftime("%Y-%m-%d %H:%M:%S"))
            result = db.execute_query(query, (choice,))

            if result:
                expenses_per_day = {day: [] for day in range(7)}

                # fill dictionary with expenses/day
                for row in result:
                    date_string = row[0].split()[0]
                    year, month, day = map(int, date_string.split('-'))
                    date = datetime(year, month, day)
                    day_of_week = date.weekday()
                    expenses_per_day[day_of_week].append(row[1])

                # calculate average
                for day, expenses in expenses_per_day.items():
                    if expenses:
                        average_expense = sum(expenses) / len(expenses)
                        print(f"Average expense for {calendar.day_name[day]}: {average_expense:.2f}")

                    else:
                        print(f"No expenses for {calendar.day_name[day]}.")

            else:
                print("No expenses found in the database.")

        except sqlite3.Error as e:
            print(f"Error calculating average expenses per day: {e}")

def average_balance(time='all'):
    try:
            # Generate entries based on delay.
            query = 'SELECT Date , Amount FROM transaction_history WHERE Date > ? ;'
            if time == 'all':
                delay = 0
            elif time == 'day':
                delay = 1
            elif time == 'week':
                delay = 7
            elif time == 'month':
                delay = 31
            elif time == 'year':
                delay = 365
            choice = str((datetime.now() - timedelta(days=delay)).strftime("%Y-%m-%d %H:%M:%S"))
            result = db.execute_query(query, (choice,))

            if result:
                total_expenses = []
    
                for row in result:
                    total_expenses.append(row[1])

                 # Calculate the average over all expenses
                if total_expenses:
                    average_expense = sum(total_expenses) / len(total_expenses)
                    print(f"Average net over all days: {average_expense:.2f}")

                else:
                    print("No expenses found in the database.")

            else:
                print("No expenses found in the database.")

    except sqlite3.Error as e:
        print(f"Error calculating average expenses per day: {e}")

