import csv
from openpyxl import Workbook
import re
import string
from pathlib import Path
from models.Database import Database

def export_to_csv(output_file):
    # give extension if not given
    normalized_filename = normalize_filename(output_file)
    normalized_filename = re.sub(r'\.csv$', '', normalized_filename) + '.csv'

    current_script_path = Path(__file__).resolve()
    exported_reports_path = current_script_path.parent / "exportedReports"
    output_path = exported_reports_path / normalized_filename
        
    # copy database
    try:
        db = Database()
        rows = db.execute_query("SELECT * FROM transaction_history;")

        with open(output_path, mode="w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            header = [description[0] for description in db.cursor.description]
            csv_writer.writerow(header)
            csv_writer.writerows(rows)

            print(f"File exported to {output_path}")

    except Exception as e:
        print(f"Database empty or not found: {e}")
    

def export_to_xlsx(output_file):
    # give extension if not given
    normalized_filename = normalize_filename(output_file)
    normalized_filename = re.sub(r'\.xlsx$', '', normalized_filename) + '.xlsx'

    current_script_path = Path(__file__).resolve()
    exported_reports_path = current_script_path.parent / "exportedReports"
    output_path = exported_reports_path / normalized_filename
        
     # copy database
    try:
        db = Database()
        rows = db.execute_query("SELECT * FROM transaction_history;")

        workbook = Workbook()
        sheet = workbook.active

        header = [description[0] for description in db.cursor.description]
        sheet.append(header)

        for row in rows:
            sheet.append(row)

        workbook.save(output_path)

        print(f"File exported to {output_path}")

    except Exception as e:
        print(f"Database leeg of niet gevonden: {e}")


# make filename usable
def normalize_filename(filename):

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c if c in valid_chars else '_' for c in filename)

    return filename


    