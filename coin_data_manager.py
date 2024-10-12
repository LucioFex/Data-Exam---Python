
import requests
import csv
import os

url_prefix = "https://api.coingecko.com/api/v3"
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-fzKFjESerjpcjNMcKPuy2WxH"
}


def get_coin_data_by_day(coin, day):
    # Coingecko GET API for 'coin' data for a given 'day'.
    formatted_day = day.strftime("%d-%m-%Y")
    url = f"{url_prefix}/coins/{coin}/history?date={formatted_day}"
    response = requests.get(url, headers=headers)
    return response.json()


def structure_coin_data_by_day(data, day):
    # Raw data structuration (dictionary format)
    coin_id = data["id"]
    symbol = data["symbol"]
    current_price_usd = data["market_data"]["current_price"]["usd"]
    market_cap_usd = data["market_data"]["market_cap"]["usd"]
    total_volume_usd = data["market_data"]["total_volume"]["usd"]
    twitter_followers = data["community_data"]["twitter_followers"]
    forks = data["developer_data"]["forks"]
    stars = data["developer_data"]["stars"]
    day_iso_8601 = day.strftime("%Y-%m-%d")  # date

    formatted_data = [
        coin_id, symbol, current_price_usd, market_cap_usd,
        total_volume_usd, twitter_followers, forks, stars, day_iso_8601
    ]
    return formatted_data


def store_new_coin_data(data, filename="coins_data.csv"):
    # TODO: With more time, it would be ideal not to show the
    # details of this implementation in this layer.

    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"{file_dir}/data/{filename}"

    existing_data = []
    rows_header = [
        'id', 'symbol', 'current_price_usd', 'market_cap_usd',
        'total_volume_usd', 'twitter_followers', 'forks', 'stars', 'date'
    ]

    file_exists = os.path.isfile(file_path)
    if file_exists:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                existing_data.append(row)
    else:
        open(file_path, 'a').close()

    # Checks if the row's row's data is repeated (by ID and Date)
    # TODO: The idea of ​​checking the first and last column to know if a row
    # is repeated or not is fragile; in an ideal situation, this should be
    # parameterized for better structure with key names (like a dict)
    for i, row in enumerate(existing_data):
        if row[0] == data[0] and row[-1] == data[-1]:
            existing_data[i] = data
            break
    else:
        # If not found, add the new row.
        existing_data.append(data)

    # Write new data in the CSV file.
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(rows_header)
        writer.writerows(existing_data)
