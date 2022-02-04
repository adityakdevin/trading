import sqlite3

import config


def update():
    connection = sqlite3.connect(config.DB_FILE)

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT * from stock_price""")

    rows = cursor.fetchall()


pass
