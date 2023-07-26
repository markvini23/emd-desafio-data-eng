import glob
import json
import os
import requests
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
import pandas as pd

import prefect
from prefect import task
from prefect.tasks.dbt import DbtShellTask
from prefect.triggers import all_successful
from prefect.engine.signals import SKIP

from sqlalchemy import create_engine
from pipeline.constants import Constants


@task(max_retries=3, retry_delay=timedelta(seconds=10))
def collect_data() -> None:
    """
    Data collection for brt gps data. Makes a request to the API and Save the result to a .json file
    """

    # Request to API
    logger = prefect.context.get("logger")
    api_url = Constants.API_URL.value
    response = requests.get(api_url)
    logger.info("Collecting Data from API...")

    # Raise status to raise a FAIL signal in case of failure on API side
    response.raise_for_status()

    #File output directory and name
    json_filename = int(datetime.now().timestamp())
    output_path = Constants.OUTPUT_DIR.value

    #Save result to a .json
    with open(f"{output_path}/{json_filename}.json", "w") as outfile:
        json.dump(response.json().get('veiculos'), outfile)

    logger.info("Json File created !")


@task(max_retries=2, retry_delay=timedelta(seconds=60))
def transform_data() -> str:
    """
        Data treatment for brt gps data. Collect list of json generated
        and aggregate into a Pandas DataFrame, converts UNIX timestamp to datetime,
        remove unused columns, create 'created_at' feature and generate .csv file.

        Returns:
            filename: str containing the .csv file generated.
    """

    #Collect json filenames into a list
    json_dir = Constants.OUTPUT_DIR.value
    json_path = os.path.join(json_dir, '*.json')
    json_file_list = glob.glob(json_path)

    #Output file
    csv_filename = int(datetime.now().timestamp())
    output_path = Constants.OUTPUT_DIR.value
    json_df_list = []

    #Condition that raises a SKIP signal to the flow execution
    #This ensure the function runs every 10 files
    if len(json_file_list) <= 10:
        raise SKIP(message='Not enough data to load into the database')

    #Collect and concatenate json objects into a DataFrame
    for p in json_file_list:
        json_df = pd.read_json(p)
        json_df['datahoracoleta'] = datetime.fromtimestamp(int(p[10:-5]))
        json_df_list.append(json_df)
        os.remove(p)

    df = pd.concat(json_df_list)

    #Date and hour treatment from unix timestamp
    df['date'] = pd.to_datetime(df['dataHora'], unit='ms').dt.tz_localize('UTC').apply(
        lambda x: x.astimezone(tzlocal())).dt.date
    df['hour'] = pd.to_datetime(df['dataHora'], unit='ms').dt.tz_localize('UTC').apply(
        lambda x: x.astimezone(tzlocal())).dt.time

    #Remove unused columns and rename columns to match postgres column names
    df.drop(columns=['dataHora', 'id_migracao_trajeto', 'direcao'], inplace=True)
    df.rename(columns={'codigo': 'codigo_onibus', 'date': 'dataposicao', 'hour': 'horaposicao'}, inplace=True)
    df.to_csv(f'{output_path}/brt_data_{csv_filename}.csv', index=False)

    return f'{output_path}/brt_data_{csv_filename}.csv'


@task(max_retries=2, retry_delay=timedelta(seconds=20), trigger=all_successful)
def load_data_to_db(filename: str) -> None:
    """Load .csv file into postgres database, it runs only when transform_data() does

    Args:
        filename : str containing the .csv filename to load to database

    """

    #Create engine for SQL insertion
    postgres_url = Constants.DB_ENGINE.value
    engine = create_engine(postgres_url)
    logger = prefect.context.get("logger")

    #Read .csv file
    df = pd.read_csv(filename)
    logger.info(f"File loaded: {filename}")
    logger.info(f"Size: {len(df)} rows inserted")

    #Load into table raw.tb_brt_gps
    df.to_sql("tb_brt_gps", engine, schema='raw', if_exists='append', index=False)


@task(max_retries=2, retry_delay=timedelta(seconds=20), trigger=all_successful, skip_on_upstream_skip=True)
def materialize_model():
    """Task to run dbt model automatically. It generates a derived table from the PostgreSQL database.
    Runs only when load_data_to_db() and transform_data() return 'Successful'

    """

    DbtShellTask(
        return_all=True,
        log_stdout=True,
        log_stderr=True,
        profile_name='default',
        environment='dev',
        profiles_dir='',
        helper_script="cd db/brt_data",
        dbt_kwargs={
            "type": "postgres",
            "host": "localhost",
            "port": 5432,
            "dbname": "brt-gps",
            "schema": "raw"
        }
    ).run(command='dbt run')
