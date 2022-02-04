import sqlite3
from pickle import FALSE

from fastapi import FastAPI, Form
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import admin.update_price as update_price
import config
import stg_supertrend

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('stock_filter', FALSE)
    script_filter = request.query_params.get('script_filter', FALSE)
    special = 'NOT NULL'
    if script_filter == 'snp_500_only':
        special = 'SNP500'
    elif script_filter == 'commodities_only':
        special = 'Futures'
    elif script_filter == 'forex_only':
        special = 'Forex'
    elif script_filter == 'indices_only':
        special = 'Indices'
    elif script_filter == 'crypto_only':
        special = 'Crypto'
    else:
        special = 'NOT NULL'

    connection = sqlite3.connect(config.DB_FILE)

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""select max(date),date from stock_price""")

    maxdate = cursor.fetchone()

    print("maxdate is ....................", maxdate['date'])
    if stock_filter == 'new_closing_highs':
        cursor.execute("""
            select * from(select max(close),* from stock_price join stock on stock.id=stock_price.stock_id WHERE Special =?
            group by stock_id
            order by Special desc
            )WHERE date= (select max(date) from stock_price)
        """, (special,))

    elif stock_filter == 'new_closing_lows':
        cursor.execute("""
            select * from(select min(close),* from stock_price join stock on stock.id=stock_price.stock_id WHERE Special =?
            group by stock_id
            order by Special desc
            )WHERE date= (select max(date) from stock_price)
        """, (special,))

    elif stock_filter == 'rsi_overbought':
        cursor.execute("""
                SELECT * FROM stock_price JOIN stock on stock.id=stock_price.stock_id
                WHERE rsi_14 > 70 AND date=(select max(date) FROM stock_price) AND Special =?
                order by symbol 
                """, (special,))

    elif stock_filter == 'rsi_oversold':
        cursor.execute("""
                SELECT * FROM stock_price JOIN stock ON stock.id=stock_price.stock_id
                WHERE rsi_14 < 30 AND date=(select max(date) FROM stock_price) AND Special =?
                ORDER BY symbol 
                """, (special,))

    elif stock_filter == 'above_sma20':
        cursor.execute("""
                select * from stock_price join stock on stock.id=stock_price.stock_id
                where close > sma_20 and sma_20 not NULL and date=(select max(date) from stock_price) AND Special =?
                order by symbol 
                """, (special,))

    elif stock_filter == 'below_sma20':
        cursor.execute("""
                select * from stock_price join stock on stock.id=stock_price.stock_id
                where close < sma_20 and sma_20 not NULL and date=(select max(date) from stock_price) AND Special =?
                order by symbol 
                """, (special,))

    elif stock_filter == 'trend_ema200':
        stg_supertrend.get_trending(special)

    else:
        cursor.execute(""" select * from(select * from  stock_price join stock on stock.id=stock_price.stock_id  
                  where date = ?)
                    """, (maxdate['date'],))

    rows = cursor.fetchall()
    indicator_rows = rows
    indicator_values = {}
    for row in indicator_rows:
        indicator_values[row['symbol']] = row

    # print(indicator_values)

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows, "stock_filter": stock_filter,
                                                     "indicators": indicator_values})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM strategy""")
    strategies = cursor.fetchall()

    cursor.execute("""SELECT id,symbol, name FROM stock WHERE symbol = ? """, (symbol,))

    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id=? ORDER BY date DESC
    """, (row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stockdetail.html",
                                      {"request": request, "stock": row, "bars": prices, "strategies": strategies})


@app.post("/apply_strategy/")
async def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    print(strategy_id, "strategy id...................")
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO stock_strategy(stock_id,strategy_id) VALUES(?,?)""", (stock_id, strategy_id))
    connection.commit()
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategies")
def strategies(request: Request):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(""" select * from strategy""")

    strategies = cursor.fetchall()
    return templates.TemplateResponse("strategies.html",
                                      {"request": request, "strategies": strategies})


@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id,name FROM strategy WHERE id=?""", (strategy_id,))
    strategy_data = cursor.fetchone()
    cursor.execute(
        """ SELECT symbol,name FROM stock JOIN stock_strategy on stock_strategy.stock_id=stock.id where strategy_id=?""",
        (strategy_id,))
    stocks = cursor.fetchall()
    return templates.TemplateResponse("strategy.html",
                                      {"request": request, "stocks": stocks, "strategy": strategy_data})


@app.get("/orders")
def strategies(request: Request):
    return templates.TemplateResponse("orders.html",
                                      {"request": request})


# @app.post("/refresh-prices")
# async def returnPrices(request: Request):
#     #populateprices.refresh_prices()
#     return {"last_updated": date.today()}


@app.get("/admin")
def strategies(request: Request):
    return templates.TemplateResponse("admin.html",
                                      {"request": request})


# @app.post("/refresh-prices")
# async def returnPrices(request: Request):
#     #populateprices.refresh_prices()
#     return {"last_updated": date.today()}


@app.get("/admin/update-price")
def admin_update_price(request: Request):
    update_price.sync()
    pass
