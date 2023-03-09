from model_build.model_building import dl_model
import string
from params import *
import requests
import pandas as pd
import numpy as np
from model_build.model_building import preprocess
from sklearn.preprocessing import RobustScaler
from params import *
BUCKET_NAME = os.environ.get("BUCKET_NAME")
import pickle

CUR_SZN_TEAMS = ['Bournemouth',
 'Everton',
 'Leeds',
 'Leicester',
 'Tottenham',
 'Crystal Palace',
 'Fulham',
 'West Ham',
 'Man United',
 'Newcastle',
 'Liverpool',
  'Brentford',
  'Brighton',
  'Chelsea',
  "Nott'm Forest",
  'Man City',
  'Arsenal',
  'Aston Villa',
  'Southampton',
  'Wolves']

def get_odds():
    response = requests.get(ODDS_API_URL).json()
    games = response[:10]

    final_lis = []
    for game in games:
        lis = []
        home_team = game['home_team']
        lis.append(home_team)
        away_team = game['away_team']
        lis.append(away_team)
        final_home_odds = []
        final_away_odds = []
        for i in range(len(game['bookmakers'])):
            home_odds = game['bookmakers'][i]['markets'][0]['outcomes'][0]['price']
            away_odds = game['bookmakers'][i]['markets'][0]['outcomes'][1]['price']
            final_home_odds.append(home_odds)
            final_away_odds.append(away_odds)
        lis.append(np.mean(final_home_odds))
        lis.append(np.mean(final_away_odds))
        final_lis.append(lis)
        df = pd.DataFrame(data=final_lis, columns=['HT', 'AT', 'AHO', 'AAO'])
        df['HT'] = df['HT'].replace(['Manchester United'], 'Man United')
        df['HT'] = df['HT'].replace(['Manchester City'], 'Man City')
        df['HT'] = df['HT'].replace(['Leicester City'], 'Leicester')
        df['HT'] = df['HT'].replace(['Leeds United'], 'Leeds')
        df['HT'] = df['HT'].replace(['Nottingham Forest'], "Nott'm Forest")
        df['HT'] = df['HT'].replace(['Tottenham Hotspur'], "Tottenham")
        df['HT'] = df['HT'].replace(['Wolverhampton Wanderers'], "Wolves")
        df['HT'] = df['HT'].replace(['West Ham United'], "West Ham")
        df['HT'] = df['HT'].replace(['Newcastle United'], "Newcastle")
        df['HT'] = df['HT'].replace(['Brighton and Hove Albion'], "Brighton")
        df['AT'] = df['AT'].replace(['Manchester United'], 'Man United')
        df['AT'] = df['AT'].replace(['Manchester City'], 'Man City')
        df['AT'] = df['AT'].replace(['Leicester City'], 'Leicester')
        df['AT'] = df['AT'].replace(['Leeds United'], 'Leeds')
        df['AT'] = df['AT'].replace(['Nottingham Forest'], "Nott'm Forest")
        df['AT'] = df['AT'].replace(['Tottenham Hotspur'], "Tottenham")
        df['AT'] = df['AT'].replace(['Wolverhampton Wanderers'], "Wolves")
        df['AT'] = df['AT'].replace(['West Ham United'], "West Ham")
        df['AT'] = df['AT'].replace(['Newcastle United'], "Newcastle")
        df['AT'] = df['AT'].replace(['Brighton and Hove Albion'], "Brighton")
    return df

def get_x_new(home_team, away_team):
    LINKS = ["mmz4281/2223/E0.csv",
             "mmz4281/2122/E0.csv"]
    df = pd.DataFrame()
    for link in LINKS:
        df = pd.concat([df, pd.read_csv(f"https://www.football-data.co.uk/{link}")]).reset_index(drop=True)
    df['THC'] = df['HY'] + df['HR']
    df['TAC'] = df['AY'] + df['AR']
    home_cols = ['HST', 'HC', 'THC']
    away_cols = ['AST', 'AC', 'TAC']
    df_home = df.groupby(df['HomeTeam'])[home_cols].mean()
    df_away = df.groupby(df['AwayTeam'])[away_cols].mean()
    home_row = df_home.loc[df_home.index==home_team]
    home_row = home_row.reset_index(drop=True)
    away_row = df_away.loc[df_away.index==away_team]
    away_row = away_row.reset_index(drop=True)
    row_final = home_row.merge(away_row, left_index=True, right_index=True)
    row_final = row_final.iloc[:, [3,0,1,4,2,5]]
    odds = pd.DataFrame(get_odds())
    home_odds = odds['AHO'].loc[odds['HT'] == home_team].values[0]
    away_odds = odds['AAO'].loc[odds['AT'] == away_team].values[0]
    row_final['AHO'] = home_odds
    row_final['AAO'] = away_odds
    return row_final

def get_input():
    print("Man United for ManU, Man City for ManC, Nott'm Forest for Nottingham Forest")
    home_team = input("Choose your home team: ")
    home_team = string.capwords(home_team, sep=None)
    away_team = input("Choose your away team: ")
    away_team = string.capwords(away_team, sep=None)
    if home_team in CUR_SZN_TEAMS:
        if away_team  in CUR_SZN_TEAMS:
            print(f"✅ Fetching recomendation for {home_team} vs {away_team}")
        else: print("❌ Away Team not found!")
    else: print("❌ Home Team not found!")
    return home_team, away_team


def dl_scaler():
    from google.cloud import storage
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="scalers"))
    blob = blobs[-1]
    pickle_in = blob.download_as_string()
    model = pickle.loads(pickle_in)
    print("✅ Scaler loaded from gcs")
    return model

def predict():
    model = dl_model()
    home_team, away_team  = get_input()
    X_new = get_x_new(home_team, away_team)
    scaler = dl_scaler()
    X_new_processed = scaler.fit_transform(X_new)
    y_pred = model.predict(X_new_processed)
    margin = y_pred[0]
    print(margin)
    if margin > 1:
        print('Bet on a Home Win')
    if margin < 1 and margin > 0:
        print("Bet on a Home Win or Draw")
    if margin > -1 and margin < 0:
        print("Bet on a Away Win or Draw")
    if margin < -1:
        print('Bet on a Away Win')

if __name__ == '__main__':
    predict()
