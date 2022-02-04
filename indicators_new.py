import sqlite3

import numpy
import pandas as pd
import talib

import config


def update(type):
    if type == 'history':
        connection = sqlite3.connect(config.DB_FILE)
        cursor = connection.cursor()
        all_stock = cursor.execute("""SELECT stock.id,stock.symbol,stock.name FROM stock""").fetchall()
        for stock in all_stock:
            print("Stock is :", stock[1])
            stock_id = stock[0]
            cursor.execute(
                """SELECT id,date,open,high,low,close FROM stock_price WHERE stock_id = ? ORDER BY id desc LIMIT 500""",
                (stock_id,))
            stock_prices = cursor.fetchall()
            counter = 0
            recent_closes = recent_lows = recent_highs = []
            for stock_price in stock_prices:
                recent_closes.append(stock_price[5])
                recent_lows.append(stock_price[4])
                recent_highs.append(stock_price[3])
                counter = counter + 1
                sma_20 = talib.SMA(numpy.array(recent_closes), timeperiod=20)
                sma_50 = talib.SMA(numpy.array(recent_closes), timeperiod=50)
                sma_100 = talib.SMA(numpy.array(recent_closes), timeperiod=100)
                sma_200 = talib.SMA(numpy.array(recent_closes), timeperiod=200)
                rsi_14 = talib.RSI(numpy.array(recent_closes), timeperiod=14)
                atr = talib.ATR(numpy.array(recent_highs), numpy.array(recent_lows), numpy.array(recent_closes),
                                timeperiod=20)
                cursor.execute(
                    """ UPDATE stock_price SET sma_20=?, sma_50=?, sma_100=?,sma_200=?, rsi_14=?,atr=? WHERE id=?""",
                    (sma_20[-1], sma_50[-1], sma_100[-1], sma_200[-1], rsi_14[-1], atr[-1], stock_price[0],))
                ## print("Record:", stock_price)
        connection.commit()

    if type == 'latest':

        connection = sqlite3.connect(config.DB_FILE)
        cursor = connection.cursor()
        all_stock = pd.read_sql_query("SELECT stock.id,stock.symbol,stock.name FROM stock", connection)
        for stock in range(len(all_stock)):
            # print("Stock is :", all_stock.loc[stock, 'symbol'], "stock number:", all_stock.loc[stock, 'name'])
            stock_id = all_stock.loc[stock, 'id']
            stock_prices = pd.read_sql_query(("SELECT id,date,open,high,low,close FROM stock_price WHERE "
                                              "stock_id = %i ORDER BY date desc LIMIT 201") % stock_id,
                                             connection)
            counter = 0
            # print("Stock is :", all_stock.loc[stock, 'symbol'], "stock number:", all_stock.loc[stock, 'id'],
            #       "stock price close =", stock_prices.iloc[0].at['close'], "stock price date=",
            #       stock_prices.iloc[0].at['date'])
            sma_20 = talib.SMA(stock_prices.close.values, timeperiod=20)
            sma_50 = talib.SMA(stock_prices.close.values, timeperiod=50)
            sma_100 = talib.SMA(stock_prices.close.values, timeperiod=100)
            sma_200 = talib.SMA(stock_prices.close.values, timeperiod=200)
            rsi_14 = talib.RSI(stock_prices.close.values, timeperiod=14)
            atr = talib.ATR(stock_prices.high.values, stock_prices.low.values, stock_prices.close.values,
                            timeperiod=20)
            print(stock_prices.iloc[-1]['date'])
            quit()
            cursor.execute(
                """UPDATE stock_price SET sma_20=?, sma_50=?, sma_100=?,sma_200=?, rsi_14=?,atr=? WHERE id=? & 
                date=?""",
                (sma_20[0], sma_50[0], sma_100[-1], sma_200[-1], rsi_14[-1], atr[-1], stock_prices.iloc[-1].at['id'],
                 stock_prices[-1].at['date']))
            connection.commit()
            break


update('latest')
