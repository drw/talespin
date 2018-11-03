import os, dataset, csv
from pprint import pprint


def clean(d):
    del d['id']
    d['uses'] = int(d['uses'])
    d['views'] = int(d['views'])
    d['usage'] = float(d['usage'])

db_filename = "/Users/drw/code/talespin/lines.sqlite"
csv_filename = "/Users/drw/code/talespin/quotes.csv"
alternate_csv_filename = "/Users/drw/code/talespin/q.csv"
assert csv_filename != alternate_csv_filename
table_name = 'talespin_lines'

#input_file = csv.DictReader(open(filename))

import os.path
db_exists = os.path.isfile(db_filename)
csv_exists = os.path.isfile(csv_filename)
if not csv_exists:
    raise ValueError("No such CSV file exists.")
if db_exists:
    raise ValueError("The target database file already exists.")

db = dataset.connect('sqlite:///{}'.format(db_filename))
table = db[table_name]

with open(csv_filename, "r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = next(reader)
    for d in reader:
        clean(d)
        table.insert(d)

print("SQLite database created from CSV file.")
os.rename(csv_filename,alternate_csv_filename)
