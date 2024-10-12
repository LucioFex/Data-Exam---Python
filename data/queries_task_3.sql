
-- Task (1): Get the average price for each coin by month.

SELECT
    coin AS "Coin",
    year AS "Year",
    TO_CHAR(TO_DATE(month::text, 'MM'), 'Month') AS "Month",
    AVG((min_price + max_price) / 2) AS "Average price"
FROM coin_month_data
GROUP BY coin, year, month
ORDER BY coin, year, month;

/* Output example:
         Coin         | Year |   Month   |    Average price
----------------------+------+-----------+---------------------
 bitcoin              | 2021 | January   |   34919.19012504335
 bitcoin              | 2021 | February  |  45367.045146966484
 bitcoin              | 2021 | March     |   53142.68069635678
...
(31 rows) */


/* Task (2): Calculate for each coin, on average, how much its price has increased after it had
dropped consecutively for more than 3 days. In the same result set include the
current market cap in USD (obtainable from the JSON-typed column). Use any time
span that you find best. */

WITH drops AS ( -- CTE to obtain loss sequences for no less than three days.
    -- NOTE: Considering that we could load separate dates for one crpyto coin,
    -- for example: '2024-08-16', '2024-08-17' and '2024-08-19' (omitting day '18'),
    -- then the next row (not day) is considered.
    SELECT
        coin,
        date,
        price,
        CASE WHEN price < LAG(price) OVER (PARTITION BY coin ORDER BY date) THEN 1 ELSE 0
        END AS is_drop,
        CASE
            WHEN LAG(price) OVER (PARTITION BY coin ORDER BY date) >= price AND
                 LAG(price, 2) OVER (PARTITION BY coin ORDER BY date) >= LAG(price)
                    OVER (PARTITION BY coin ORDER BY date) AND
                 LAG(price, 3) OVER (PARTITION BY coin ORDER BY date) >= LAG(price, 2)
                    OVER (PARTITION BY coin ORDER BY date)
            THEN 1
            ELSE 0
        END AS consecutive_drop_3
    FROM coin_data
),
drop_periods AS ( -- Filter of the consecutive drops in periods of three days (technically "rows")
    SELECT
        coin,
        date,
        price,
        LEAD(price) OVER (PARTITION BY coin ORDER BY date) AS following_price,
        consecutive_drop_3
    FROM drops
    WHERE consecutive_drop_3 = 1
),
price_increase AS ( -- Verification of the price increase the day after the end of a "loss" (drop) period.
    SELECT
        coin,
        AVG(following_price - price) AS avg_price_increase
    FROM drop_periods
    WHERE following_price > price
    GROUP BY coin
)
SELECT
    p.coin AS "Coin",
    p.avg_price_increase "Price increase in USD (1 day)",
    c.json->'market_data'->'market_cap'->>'usd' AS "Market cap in USD"
FROM price_increase p
INNER JOIN (
    SELECT DISTINCT ON (coin) coin, json
    FROM coin_data
    ORDER BY coin, date DESC
) c ON p.coin = c.coin;

/* Output example:
   Coin   | Price increase in USD (1 day) | Market cap in USD
----------+-------------------------------+-------------------
 bitcoin  |             6505.980890466838 | 1176063402361.815
 cardano  |           0.30420450098266905 | 11993838867.74028
 ethereum |             725.4749766337344 | 317616756579.9527
(3 rows) */
