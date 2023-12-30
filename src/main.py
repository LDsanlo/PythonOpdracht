from models.Database import Database

def main():

    db = Database()
    db.insert_row(100.0, "Test description")
    db.read_all_rows()
    db.delete_last_row()

    while True:
        input_user = input("What would you like to do? ('q' to exit):").strip().lower()
        if input_user == 'q':
            print("Goodbye!")
            break

        elif input_user == 'help':
            with open('methods.txt', 'r') as file:
                content = file.read()
                print(content)

        elif input_user == 'addcost':
            a = input('How much?:')
            b = input('Cost description:')
            db.insert_row(a,b)

        elif input_user == 'printdatabase':
            db.read_all_rows()


if __name__ == "__main__":
    main()