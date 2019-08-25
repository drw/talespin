import os, dataset, datafreeze

from tell import db_filename
alternate_filename = "/Users/drw/code/talespin/l.sqlite"
assert db_filename != alternate_filename
table_name = 'talespin_lines'


import os.path
db_exists = os.path.isfile(db_filename)
if not db_exists:
    raise ValueError("No such database exists.")
db = dataset.connect('sqlite:///{}'.format(db_filename))
result = db[table_name].all()
datafreeze.freeze(result, format='csv', filename='quotes.csv')
os.rename(db_filename,alternate_filename)
