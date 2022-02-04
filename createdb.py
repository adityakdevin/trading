import sqlite3

import config

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            symbol  TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            exchange TEXT NOT NULL,
            last_date TEXT,
            Special TEXT
        )
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_price(
            id INTEGER PRIMARY KEY,
            stock_id INTEGER,
            date NOT NULL,
            open NOT NULL,
            high NOT NULL,
            low NOT NULL,
            close NOT NULL,
            volume NOT NULL,
            sma_20,
            sma_50,
            sma_100,
            sma_200,
            rsi_14,
            atr,
            ema_20,
            ema_50,
            ema_100,
            ema_200,
            FOREIGN KEY (stock_id) references stock (id)
        )
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy (
            id INTEGER PRIMARY KEY,
            name  NOT NULL
            )
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_strategy (
            stock_id INTEGER NOT NULL,
            strategy_id INTEGER NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id),
            FOREIGN KEY (strategy_id) REFERENCES strategy (id)
        )
    """)
cursor.execute("""
        CREATE TABLE IF NOT EXISTS stockdaily (
            id INTEGER PRIMARY KEY,
            symbol  TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            exchange TEXT NOT NULL,
            last_date TEXT
        )
    """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices_daily (
            id INTEGER PRIMARY KEY,
            stock_id INTEGER,
            date NOT NULL,
            open NOT NULL,
            high NOT NULL,
            low NOT NULL,
            close NOT NULL,
            volume NOT NULL,
            FOREIGN KEY (stock_id) references stock_daily (id)
            )
        """)

cursor.execute("""
        CREATE TABLE "stock_super_trend_daily" (
                "id"	INTEGER,
                "stock_id"	INTEGER NOT NULL,
                "date"	TEXT NOT NULL,
                "open"	TEXT NOT NULL,
                "high"	TEXT NOT NULL,
                "low"	TEXT NOT NULL,
                "close"	TEXT NOT NULL,
                "volume"	TEXT NOT NULL,
                "buy"	TEXT,
                "sell"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("stock_id") REFERENCES "stock"("id")
            );
        """)

strategies = ['opening_range_breakout', 'opening_range_breakdown']

for strategy in strategies:
    cursor.execute("""  
            INSERT INTO strategy (name) VALUES (?)""", (strategy,))

connection.commit()
