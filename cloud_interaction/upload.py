from google.cloud import bigquery
import pandas as pd
from import_pack.import_data import grab_epl_data
from odds_featuring.odds_features import get_odds_final
from stats_pack.stats_features import stats_features
from average_pack.average import get_averages
import os
import pickle
import time
from params import *

local_path = LOCAL_REGISTRY_PATH
BUCKET_NAME = os.environ.get("BUCKET_NAME")

def upload_model(model):
    from google.cloud import storage
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # save model locally
    model_path = os.path.join(local_path, f"{timestamp}.pkl")
    with open(model_path,'wb') as f:
        pickle.dump(model,f)

    print("✅ Model saved locally")


    # 🎁 We give you this piece of code as a gift. Please read it carefully! Add breakpoint if you need!


    model_filename = model_path.split("/")[-1] # e.g. "20230208-161047.h5" for instance
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"models/{model_filename}")
    blob.upload_from_filename(model_path)

    print("✅ Model saved to gcs")
    return None

def upload_historic_data():
    """
    This function will return data that is selected but not preprocessed
    """
    PROJECT = "predicting-epl-results"
    DATASET = "processed_data"
    TABLE = "processed"

    table = f"{PROJECT}.{DATASET}.{TABLE}"

    df = grab_epl_data()
    df_final = stats_features(df).join(get_odds_final(df)).drop(columns=['margin'])
    df_final = df_final.dropna()
    df_final['idx'] = [i+1 for i in range(len(df_final))]
    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" # or "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(df_final, table, job_config=job_config)
    result = job.result()
    return None



def upload_raw_data():
    PROJECT = "predicting-epl-results"
    DATASET = "raw_data"
    TABLE = "updated_game_history"
    raw_data_columns = ['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',\
       'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HS', 'AS', 'HST', 'AST',\
       'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D',\
       'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD',\
       'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'idx']
    table = f"{PROJECT}.{DATASET}.{TABLE}"

    df = grab_epl_data()
    # df = df.dropna()
    df['idx'] = [i+1 for i in range(len(df))]
    df = df[raw_data_columns]
    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" # or "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(df, table, job_config=job_config)
    result = job.result()
    return None

def upload_averages():
    PROJECT = "predicting-epl-results"
    DATASET = "average_data"
    TABLE = "home_averages"
    TABLE2 = "away_averages"

    table = f"{PROJECT}.{DATASET}.{TABLE}"

    df_home, df_away = get_averages()

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" # or "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(df_home, table, job_config=job_config)
    result = job.result()
    return None

if __name__ == '__main__':
    # upload_historic_data()
    # upload_raw_data()
    upload_model()
