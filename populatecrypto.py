import yfinance as yf
import datetime
import config
import pandas
import sqlite3
today=datetime.date.today().isoformat()
connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

companies=pandas.read_csv(config.CRYPTO_FILE)
print(companies)

for i in companies.index:
    symbol=companies['Symbol'][i]
    cursor.execute("""INSERT or Replace INTO stock (symbol,name,special,exchange) VALUES(?,?,?,?)""",
                           (companies['Symbol'][i], companies['Name'][i], 'Crypto','YFinance',))
df={}
connection.commit()
 