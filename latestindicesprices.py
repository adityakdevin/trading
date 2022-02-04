import config
import pandas
import sqlite3
import yfinance as yf
from datetime import timedelta, date, datetime


def updatePrice(max_price):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT id,symbol, name from stock where Special='Indices'""")
    rows = cursor.fetchall()
    symbols = []
    stock_dict = {}
    for row in rows:
        symbol = row['symbol']
        symbols.append(symbol)
        stock_dict[symbol] = row['id']
    companies = pandas.read_csv(config.INDICES_FILE)
    totalUpdatedPrice = 0
    for i in companies.index:
        symbol = companies['Symbol'][i]
        df = yf.download(symbol, start="2000-09-01", end=date.today().isoformat())
        for df_date, j in df.iterrows():
            date_value = df_date.strftime('%Y-%m-%d')
            stock_id = stock_dict[symbol]
            try:

                cursor.execute(
                    """INSERT or REPLACE INTO stock_price (stock_id,date,open,high,low,close,volume) VALUES (?,?,?,?,
                    ?,?,?)""",
                    (stock_id, date_value, j['Open'], j['High'], j['Low'], j['Close'], j['Volume']))
                totalUpdatedPrice += totalUpdatedPrice
            except:
                pass
    connection.commit()
    return totalUpdatedPrice
