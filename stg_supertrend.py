import sqlite3

import pandas as pd
import pandas_ta as ta

import config


def get_trending(special):
    con = sqlite3.connect(config.DB_FILE)
    # stocks = pd.read_sql_query("""SELECT stock.id,stock.symbol,stock.name FROM stock where Special= '%s'""" % special,
    #                            con)
    stocks = pd.read_sql_query("""SELECT stock.id,stock.symbol,stock.name FROM stock""",
                               con)
    trending_stocks = stocks
    trend = False
    trending_stocks.rename(columns={'id': 'stock_id'}, inplace=True)
    # print(trending_stocks.head())
    dftrend = pd.DataFrame()
    for i in range(len(stocks)):
        df = pd.DataFrame()
        super = pd.DataFrame()
        stock_id = stocks.loc[i, 'stock_id']
        # print("stock id is :", stock_id)
        con = sqlite3.connect(config.DB_FILE)
        df = pd.read_sql_query(
            "select * from (SELECT stock_id,id,date,open,high,low,close FROM stock_price WHERE stock_id = %i order by "
            "id desc limit 20) order by date asc " % stock_id,
            con, )
        if i == 0:
            dftrend = pd.DataFrame(data=None, columns=df.columns, index=df.index)

        try:
            super.insert(0, 'signal',
                         ta.supertrend(high=df['high'], low=df['low'], close=df['close'], period=7, multiplier=3)[
                             'SUPERT_7_3.0'])
        except:
            pass
        df.insert(len(df.columns), 'buy_signal', 0)
        df.insert(len(df.columns), 'sell_signal', 0)

        trend = False
        n = 10

        for j in range(len(df) - 3, len(df)):
            if df['close'][j - 1] <= super['signal'][j - 1] and df['close'][j] > super['signal'][j]:
                df.at[j, 'buy_signal'] = 1

                # trending_stocks.append(stock_id,df['date'],df['close'][i],df['high'][i],df['low'],df['buy_signal'][i],df['sell_signal'][i])
                trend = True

            if df['close'][j - 1] >= super['signal'][j - 1] and df['close'][j] < super['signal'][j]:
                df.at[j, 'sell_signal'] = 1

                trend = True

        if trend == True:
            dftrend = pd.concat([dftrend, df], ignore_index=True)
            # print(dftrend)

    trending_stocks = pd.merge(trending_stocks, dftrend)
    trending_stocks.dropna()
    s = trending_stocks
    selectedstocks = pd.DataFrame()
    # print(s.shape)

    for index1, row1 in s.iterrows():

        if row1['buy_signal'] == 1 or row1['sell_signal'] == 1:
            selectedstocks = selectedstocks.append(row1, ignore_index=True)

    print(selectedstocks)
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()
    for index2, row2 in selectedstocks.iterrows():
        cursor.execute(
            """INSERT or Replace INTO stock (stock_id,date,open,high,low,close,volume,buy,sell) 
            VALUES(?,?,?,?,?,?,?,?,?)""",
            ('1', row2['Date'], row2['Open'], row2['High'], row2['Low'], row2['Close'], row2['Volume']))

    connection.commit()


get_trending('SN500')
