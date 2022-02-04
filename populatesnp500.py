import sqlite3

import alpaca_trade_api as tradeapi

import config
import csv

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""select * from stock""")

stocks = cursor.fetchall()


# print(symbols)
symbols_snp=[]
stock_ids={} 
stocks_snp={}

with open(config.SNP_FILE) as f:
    reader=csv.reader(f)
    for line in reader:
        symbols_snp.append(line)

 
for stock in stocks:
    symbol=stock['symbol']
    stock_ids[symbol]=stock['id']
    for row in symbols_snp:
        if row[0] == symbol:
            cursor.execute("""update stock set special="SNP500" where symbol=?""",(symbol,))
            connection.commit 
       
 
 

 

# api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
# assets = api.list_assets()

# for asset in assets:
#     try:
#         if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
#             print(f"Added a new stock {asset.symbol} {asset.name}")
#             cursor.execute("INSERT INTO stock (symbol,name,exchange) VALUES(?,?,?)",
#                            (asset.symbol, asset.name, asset.exchange))
#     except Exception as e:
#         print(asset.symbol)
#         print(e)

connection.commit()