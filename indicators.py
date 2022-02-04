import sqlite3
import numpy
import talib
import config


def update(update_type):
    if update_type == 'history':
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
        connection.commit()

    if update_type == 'latest':
        connection = sqlite3.connect(config.DB_FILE)
        cursor = connection.cursor()
        all_stock = cursor.execute("""SELECT stock.id,stock.symbol,stock.name FROM stock""").fetchall()
        for stock in all_stock:
            print("Stock is :", stock[1], "stock number:", stock)
            stock_id = stock[0]
            cursor.execute(
                """SELECT id,date,open,high,low,close FROM stock_price WHERE stock_id = ? ORDER BY id desc LIMIT 201""",
                (stock_id,))
            stock_prices = cursor.fetchall()
            counter = 0
            recent_closes = recent_lows = recent_highs = []
            for stock_price in stock_prices:
                recent_closes.append(stock_price[5])
                recent_lows.append(stock_price[4])
                recent_highs.append(stock_price[3])
                counter = counter + 1
                if counter > 480:
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
