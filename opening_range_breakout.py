import sqlite3
import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from datetime import date,datetime 
import requests
import smtplib,ssl

context=ssl.creat_default_context()




connection=sqlite3.connect(config.DB_FILE)
connection.row_factory=sqlite3.Row

min_bars_url=config.BARS_URL+'/5Min?symbols=MSFT'
r=requests.get(min_bars_url,headers=config.HEADERS)
print(r.content)

cursor=connection.cursor()

cursor.execute("""
    select id from strategy where name='opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    select  symbol,name
    from stock
    join stock_strategy on stock_strategy.stock_id = stock.id
    where stock_strategy.strategy_id=?  
""",(strategy_id,))

stocks=cursor.fetchall()

symbols= [stock['symbol'] for stock in stocks]

print(symbols)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
current_date=datetime.today().isoformat() 
start_minute_bar=f"{current_date} 09:30:00-04:00"
end_minute_bar=f"{current_date} 09:45:00-04:00"

orders=api.list_orders(status='all',after=f"{current_date}T13:30:00Z")
existing_order_symbols=[order.symbol for order in orders]

messages= []

for symbol in symbols:

    if symbol not in existing_order_symbols:

        minute_bars=api.polygon.historic_agg_v2(symbol,1,'minute',_from=current_date, to= current_date).df
        opening_range_mask=(minute_bars.index>= start_minute_bar) & (minute_bars.index <end_minute_bar)
        opening_range_bars=minute_bars.loc[opening_range_bars]

        opening_range_low=opening_range_bars['low'].min()
        opening_rang_high=opening_range_bars['high'].max()

        opening_range=opening_rang_high-opening_range_low

        after_opening_range_mask=minute_bars.index>=end_minute_bar

        after_opening_range_bars=minute_bars.loc[after_opening_range_mask]

        int(after_opening_range_bars)

        after_opening_range_breakout=after_opening_range_bars[after_opening_range_bars['close']>opening_rang_high]

        if not after_opening_range_breakout.empty:
            limit_price= after_opening_range_breakout.iloc[0]['close']

            messages.append(f"placing order for {symbol} at {limit_price}, closed_above {opening_rang_high} \n\n at {after_opening_range_breakout}\n\n")

            print(f"placing order for {symbol} at {limit_price}, closed_above {opening_rang_high} at {after_opening_range_breakout}")
            
            api.submit.order(
                symbol= symbol,
                side='buy',
                type='limit',
                qty='100',
                time_in_force='day',
                order_class='bracket',
                limit_price=limit_price,
                take_profit=dict(
                    limit_price=limit_price+opening_range,
                ),

                stop_loss=dict(
                    stop_price=limit_price-opening_range,
                )

            
            )
            

    else:
        print(f"Already an order for {symbol} skipping")

with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORTport, context=context) as server:
    server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

    email_message=f"Subject: Trade test for {current_date} \n\n"
    email_message="\n\n".join(messages)

    server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, email_message)
