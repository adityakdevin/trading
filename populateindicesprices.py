from datetime import timedelta,date,datetime
import config
import pandas
import sqlite3
import yfinance as yf


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

companies=pandas.read_csv(config.INDICES_FILE)


for i in companies.index:
    symbol = companies['Symbol'][i]
  
 
    df = yf.download(symbol, start="2000-09-01", end=date.today().isoformat())
    for i, j in df.iterrows():
        datevalue=i.strftime('%Y-%m-%d')
        stock_id = stock_dict[symbol]
        # print("date is ",datevalue,symbol,stock_id)
        # print(i,j) 
        stock_id = stock_dict[symbol]

        try:
         
            cursor.execute(
                        """ INSERT or REPLACE INTO stock_price (stock_id,date,open,high,low,close,volume) VALUES (?,?,?,?,?,?,?)""",
                        (stock_id, datevalue, j['Open'],j['High'], j['Low'], j['Close'], j['Volume']))
        
        except:
            pass
connection.commit()