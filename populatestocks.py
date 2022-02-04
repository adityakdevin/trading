import sqlite3

import alpaca_trade_api as tradeapi

import config

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""select symbol, name from stock""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]
print(symbols)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol,name,exchange) VALUES(?,?,?)",
                           (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()
