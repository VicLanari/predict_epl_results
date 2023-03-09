from google.cloud import bigquery
import pandas as pd
from import_pack.import_data import grab_epl_data
from odds_featuring.odds_features import get_odds_final
from stats_pack.stats_features import stats_features

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

if __name__ == '__main__':
    upload_historic_data()
    upload_raw_data()
