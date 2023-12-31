import os
import sqlite3
import random
from datetime import datetime, timedelta
from datetime import datetime

class Database:
    def __init__(self):

        # zoek pad naar map 'database'
        current_script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(current_script_path)
        database_directory = os.path.join(script_directory, "..", "database")
        self.path = os.path.join(database_directory, "database.db")

        self.connection = None
        self.cursor = None
        self.connect()
        balance = self.calculate_balance()
        
    def connect(self):
        try:
            #kijk of de database aanwezig is in de map 'database', zoniet, maak een nieuwe aan
            if not os.path.exists(self.path):
                self.create_database()

            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def create_database(self):
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS transaction_history (
                id INTEGER PRIMARY KEY,
                Date TEXT,
                Amount REAL,
                Description TEXT
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Database created successfully")

        except sqlite3.Error as e:
            print(f"Error creating the database: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return []

    def insert_row(self, amount, description):
        try:
            table_name = "transaction_history"
            columns = "Date, Amount, Description"
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = (date, amount, description)

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({','.join(['?' for _ in values])})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Row inserted successfully")

        except sqlite3.Error as e:
            print(f"Error inserting row: {e}")

    def delete_last_row(self):
        try:
            query = "DELETE FROM transaction_history WHERE id = (SELECT MAX(id) FROM transaction_history);"
            self.cursor.execute(query)
            self.connection.commit()
            print("Last row deleted successfully")

        except sqlite3.Error as e:
            print(f"Error deleting last row: {e}")

    def calculate_balance(self):
        try:
            query = "SELECT Amount FROM transaction_history;"
            result = self.execute_query(query)

            numeric_values = [float(row[0]) for row in result if row[0] is not None]
            second_row_sum = sum(numeric_values)

            return round(second_row_sum,2)
        
        except sqlite3.Error as e:
            print(f"Error calculating sum of the second row: {e}")
            return None

# code for making a new realistic database, to use this, give insert_row the parameter 'date' and put the date line (69) in #
    def populate_data(self):
        for _ in range(440):
            date = self.generate_random_date()
            amount = self.generate_random_amount()
            self.insert_row(date, amount, "Expense")

        current_date = datetime.now()

        for _ in range(52):
            date = current_date.strftime("%Y-%m-%d %H:%M:%S")
            self.insert_row(date, 60, "Income")
            current_date -= timedelta(weeks=1)

    def generate_random_date(self):
        current_date = datetime.now()
        random_days = random.randint(1, 365)
        new_date = current_date - timedelta(days=random_days)

        return new_date.strftime("%Y-%m-%d %H:%M:%S")

    def generate_random_amount(self):
        return random.uniform(-5, -20)
