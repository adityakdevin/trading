import datetime
import sqlite3

import pandas

import config

today = datetime.date.today().isoformat()
connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

companies = pandas.read_csv(config.FUTURES_FILE)
print(companies)

for i in companies.index:
    symbol = companies['Symbol'][i]
    cursor.execute("""INSERT or Replace INTO stock (symbol,name,special,exchange) VALUES(?,?,?,?)""",
                   (companies['Symbol'][i], companies['Future'][i], 'Futures', 'YFinance',))
df = {}
connection.commit()
