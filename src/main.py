from models.Database import Database
import modules.Statisticsdb as st
from reports.export import export_to_csv
from reports.export import export_to_xlsx

def main():
    db = Database()

    while True:
        input_user = input("What would you like to do? ('q' to exit):").strip().lower()
        if input_user == 'q':
            print("Goodbye!")
            break

        elif input_user == 'help':
            with open('textFiles\methods.txt', 'r') as file:
                content = file.read()
                print(content)

        elif input_user == 'addcost':
            a = input('How much?:')
            b = input('Cost description:')
            db.insert_row(a,b)

        elif input_user == 'dellast':
            db.delete_last_row()

        elif input_user == 'calcbal':
            print(db.calculate_balance())

        elif input_user == 'csv':
            name = input('Name of the csv file:')
            export_to_csv(name)

        elif input_user == 'xlsx':
            name = input('Name of the xlsx file:')
            export_to_xlsx(name)

        elif input_user == 'avgexp':
            time = input('For how long ago:')
            st.average_expenses(time)
        
        elif input_user == 'avgnet':
            time = input('For how long ago:')
            st.average_balance(time)

if __name__ == "__main__":
    main()