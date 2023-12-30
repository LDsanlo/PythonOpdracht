from models.Database import Database

def main():

    db = Database()
    db.insert_row("2023-01-01", 100.0, "Test description")
    db.read_all_rows()
    db.delete_last_row()
    print("test")

if __name__ == "__main__":
    main()