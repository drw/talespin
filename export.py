import os, dataset, datafreeze

filename = "/Users/drw/code/talespin/lines.db"
table_name = 'talespin_lines'


import os.path
db_exists = os.path.isfile(filename)
if not db_exists:
    raise ValueError("No such database exists.")
db = dataset.connect('sqlite:///{}'.format(filename))
result = db[table_name].all()
datafreeze.freeze(result, format='csv', filename='quotes.csv')
