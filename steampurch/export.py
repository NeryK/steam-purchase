"""Export Steam purchase history data"""

import json
import csv

def write_json_file(json_file_path, data):
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps([transaction._asdict() for transaction in data]))

def write_csv_file(csv_file_path, data):
    with open(csv_file_path, "w", encoding="utf-8", newline="\n") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0]._fields)
        writer.writeheader()
        for transaction in data:
            writer.writerow(transaction._asdict())
