
from datetime import date
import json
import psycopg2

# Note on using two libraries to manage the database:
# You will notice that I have used psycopg2 and sqlalchemy,
# one for this manager, and the other for Jupyter Notebook.

# My idea with this is to demonstrate my skills in jumping from a
# driver like psycopg2 to an ORM like sqlalchemy,
# not exactly having the most optimized set of tools (for this exam).


def db_connection():
    # TODO: The credentials should NOT be in the file, they should be
    # used with environment variables (with libraries like dotenv).
    return psycopg2.connect(
        host="localhost",
        port="5435",
        database="mutt_exam",
        user="mutt_ex",
        password="mutt_am"
    )


def store_coin_data_in_db(coin_name, raw_date, data, price_usd):
    # TODO: This function should be more modularized,
    # separating the data extraction from the data storage.
    conn = db_connection()
    with conn:
        with conn.cursor() as cursor:
            # Check if the row exists in the "coin_data" table.
            cursor.execute("""
                SELECT 1 FROM coin_data WHERE coin = %s AND date = %s;
            """, (coin_name, raw_date))
            exists = cursor.fetchone()

            json_data = json.dumps(data)
            if exists:
                # If it exists, update the row.
                cursor.execute("""
                    UPDATE coin_data
                        SET price = %s, json = %s
                    WHERE coin = %s AND date = %s;
                """, (price_usd, json_data, coin_name, raw_date))
            else:
                # If it doesn't exist, insert a new row.
                cursor.execute("""
                    INSERT INTO coin_data (coin, date, price, json)
                        VALUES (%s, %s, %s, %s);
                """, (coin_name, raw_date, price_usd, json_data))

            # Year and month extraction:

            # TODO: 'Date' has been converted twice and could be optimized.
            day = date.fromisoformat(raw_date)
            year = day.year
            month = day.month

            # Check if the row exists in coin_month_data table.
            cursor.execute("""
                SELECT min_price, max_price
                FROM coin_month_data
                WHERE coin = %s AND year = %s AND month = %s;
            """, (coin_name, year, month))
            result = cursor.fetchone()

            if result:
                # If there's at least one row,then update the min/max prices.
                current_min, current_max = result
                new_min = min(current_min, price_usd)
                new_max = max(current_max, price_usd)

                cursor.execute("""
                UPDATE coin_month_data
                    SET min_price = %s, max_price = %s
                WHERE coin = %s AND year = %s AND month = %s;
                """, (new_min, new_max, coin_name, year, month))
            else:
                # If there's not another row, insert a new one.
                cursor.execute("""
                INSERT INTO coin_month_data
                    (coin, year, month, min_price, max_price)
                    VALUES (%s, %s, %s, %s, %s);
                """, (coin_name, year, month, price_usd, price_usd))
        conn.commit()
