import os
import sqlite3
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

    def connect(self):
        try:
            #kijk of de database aanwezig is in de map 'database', zoniet, maak een nieuwe aan
            if not os.path.exists(self.path):
                self.create_database()

            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            print(f"Connected to the database at {self.path}")
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
            date = datetime.now().strftime("%H:%M:%S")
            values = (date, amount, description)

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({','.join(['?' for _ in values])})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Row inserted successfully")
        except sqlite3.Error as e:
            print(f"Error inserting row: {e}")

    def read_all_rows(self):
        try:
            query = "SELECT * FROM transaction_history;"
            result = self.execute_query(query)
            
            if result:
                for row in result:
                    print(row)
            else:
                print("No rows found in the database.")

        except sqlite3.Error as e:
            print(f"Error reading rows from the database: {e}")

    def delete_last_row(self):
        try:
            query = "DELETE FROM transaction_history WHERE id = (SELECT MAX(id) FROM transaction_history);"
            self.cursor.execute(query)
            self.connection.commit()
            print("Last row deleted successfully")

        except sqlite3.Error as e:
            print(f"Error deleting last row: {e}")

