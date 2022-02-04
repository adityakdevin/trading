import sqlite3
from datetime import date

import yfinance as yf

import config


def updatePrice(max_date):
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""SELECT count(id) from stock where Special IS NULL OR Special='SNP500'""")
    rows = cursor.fetchall()
    totalUpdatedPrice = 0
    for row in rows:
        df = yf.download(row[1], start=max_date, end=date.today().isoformat())
        for df_date, j in df.iterrows():
            date_value = df_date.strftime('%Y-%m-%d')
            stock_id = row[0]
            try:
                cursor.execute(
                    """INSERT or REPLACE INTO stock_price (stock_id,date,open,high,low,close,volume) VALUES (?,?,?,?,
                    ?,?,?)""",
                    (stock_id, date_value, j['Open'], j['High'], j['Low'], j['Close'], j['Volume']))
                totalUpdatedPrice += 1
            except:
                pass
    connection.commit()
    return totalUpdatedPrice
