# Data Dev Exam
## Technical Exam Overview

1. **Getting crypto token data**
2. **Loading data into the database**
3. **Analysing coin data with SQL**
4. **Finance meets Data Science**

### Technologies used and installation

#### Python: `3.10.12` 🐍

| Library     | Version |
| ----------- | ------- |
| requests    | 2.32.3  |
| typer       | 0.12.4  |
| psycopg2    | 2.9.9   |
| jupyter     | 1.0.0   |
| pandas      | 2.2.2   |
| matplotlib  | 3.9.2   |
| SQLAlchemy  | 2.0.32  |

In the project's files, you will find a `Pipfile` that includes all these libraries in their specific versions. If you have installed `pipenv`, you can run `pipenv install` to install the dependencies in the environment, and activate it with `pipenv shell`.

If you have a problem installing the dependencies because of _psycopg2_, that means that you could need to install the following dependency of this library `libpq-dev`.
```bash
# In the case you have this previous error, install `libpq-dev` (example with Linux/Ubuntu).
sudo apt-get install libpq-dev
```

#### PostgreSQL: `16.4` (with Docker 🐋)

You'll also find a `docker-compose.yml` file that sets up the database, user, password, and tables (including the data provided in the repository).

* **Database name:** `data_exam`
* **Local port:** `5435`
* **Test user credentials:**
  * **Name:** `data_ex`
  * **Password:** `data_am`

To activate the container with the database, run `docker compose up -d` in the project's main directory. Additionally, if you want to connect to the database via CLI, you can run:

```bash
psql -h localhost -p 5435 -U data_ex -d data_exam
```


### Usage

Once everything is set up, you can run two different commands using the `main.py` file:

* `today-info` (accepts two parameters)
* `day-info` (accepts no parameters and is also used by the CRON)

#### day-info Command

The `day-info` extracts data about Cryptocurrencies from CoinGecko, and it does transform it and load it into a local CSV for every execution (and opcionally, the database):
This command has two parameters.

* `coin` - The name of a cryptocurrency accepted by the CoinGecko API.
* `date` - The date in ISO 8601 format.

Additionally, it includes an optional flag:

* `db-store` - If set, this flag updates both the local CSV and the database.

The CSV file will be stored in the '**data**' folder with the name 'coins_data.csv'.

Here are a few examples:

```bash
python main.py day-info ethereum 2024-08-19
python main.py day-info cardano 2024-07-31 --db-store
```

#### today-info Command

This command does the same as **day-info**, but without requiring any parameters. It automatically extracts, transforms, and loads data for three cryptocurrencies: Bitcoin, Ethereum, and Cardano with the current date. This command is also scheduled to run daily at 3 AM via CRON.

Here's an example:
```bash
python main.py today-info --db-store
```

### Cron

To enable the CRON job, run `crontab -e` and add the following line to schedule the `today-info` command to run every day at 3 AM.

```bash
# every minute | every hour | every day of the month | every month of the year | every day of the week
0 3 * * * /usr/bin/pipenv run python /your_data_path/main.py today-info --db-store
```

If it doesn't work, check if it is not activated in bash.
```bash
service cron status # Cron check.
sudo systemctl enable cron # Cron enable if it was disabled.
```

### About Exercises 3 and 4

* For the third exercise, the queries to run in PostgreSQL are located in the `queries_task_3.sql` file inside the '**data**' folder.
* For the fourth exercise, you'll find a Jupyter Notebook file in the main folder that contains the first part of the exercise.
  * Additionally, plots will be generated in the '**plots**' folder; three example plots are already included by default.
  * To update the database with recent data without manually running the `main.py` file multiple times, I've included a `exercise_4_help.sh` script. This script contains useful snippets and additional information to save you time.
