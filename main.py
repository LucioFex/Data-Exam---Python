
import typer
from datetime import date
import coin_data_manager as cdm
import db_management as dm

app = typer.Typer()


def obtain_and_store_coin_data(coin_name: str, input_date: str, db_store: bool):
    try:
        # Validation of the ISO 8601 date format.
        day = date.fromisoformat(input_date)
        data = cdm.get_coin_data_by_day(coin_name, day)
        structured_data = cdm.structure_coin_data_by_day(data, day)

        # Store data in the local 'coins_data.csv' file.
        cdm.store_new_coin_data(structured_data)

        # Store data in the local database.
        if db_store:
            dm.store_coin_data_in_db(
                coin_name, input_date, data, structured_data[2]
            )

    except ValueError as e:
        # If the date is not in ISO 8601 format, an error will be raised.
        typer.echo(
            "* ERR: Wrong date format, ISO 8601 expected." +
            f"\n* HINT: {e}, expected YYYY-MM-DD"
        )
        raise typer.Exit(code=1)


@app.command()  # CLI: today-info (this command is used by the CRON).
def today_info(db_store: bool = False):
    # Input data to obtain data
    today = date.today().isoformat()
    coins = ['bitcoin', 'ethereum', 'cardano']

    for coin_name in coins:
        obtain_and_store_coin_data(coin_name, today, db_store)

    # TODO: Calling the API three times is unnecessarily expensive, but
    # CoinGecko does not support the "/coins" endpoint for more than one
    # specific "coin". (I'll leave it like this because it's an exam)
    # An alternative with different data would be the following:
    # https://api.coingecko.com/api/v3/coins/markets?vs_currency=ars&ids=bitcoin,ethereum,cardano&order=market_cap_desc&per_page=3&page=1&sparkline=false


@app.command()  # CLI: day-info
def day_info(coin_name: str, input_date: str, db_store: bool = False):
    obtain_and_store_coin_data(coin_name, input_date, db_store)


if __name__ == "__main__":
    app()
