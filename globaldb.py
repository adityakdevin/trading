import config
import sqlite3
from datetime import date


def getMaxDate():
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""SELECT max(date) as max_date from stock_price""")
    row = cursor.fetchone()
    if row[0] is None:
        return date.today().isoformat()
    else:
        return row[0]
