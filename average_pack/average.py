
import pandas as pd
from import_pack.import_data import *
from stats_pack.stats_features import stats_features

def get_averages():
    df = grab_epl_data()
    df['margin'] = df['FTHG'] - df['FTAG']
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.loc[df['Date'] > '2022/07/01']

    df_home = df.groupby(df['HomeTeam']).mean()
    df_home['THC'] = df_home['HY'] + df_home['HR']
    df_home = df_home[['HST', 'THC', 'HC']]

    df_away = df.groupby(df['AwayTeam']).mean()
    df_away['TAC'] = df_away['AY'] + df_away['AR']
    df_away = df_away[['AST', 'TAC', 'AC']]

    return df_home, df_away
