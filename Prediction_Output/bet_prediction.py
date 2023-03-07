from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import pandas as pd
from import_pack.import_data import *
from odds_featuring.odds_features import get_odds_final
from stats_pack.stats_features import stats_features
from model_build.model_building import *


df = grab_epl_data()
df_final = data_prepare_for_split(df)

X_train, X_test, y_train, y_test = tt_split(df_final)

X_train_processed, X_test_processed = preprocess(X_train, X_test)

model = initialize_model()

model = train_model(model, X_train_processed, y_train)

def predict_bet(X_new):
    y_pred = model.predict(X_new)
    if y_pred > 1:
        print('Bet on a Home Win')
    if y_pred < 1 and y_pred > 0:
        print("Bet on a Home Win or Draw")
    if y_pred > -1 and y_pred < 0:
        print("Bet on a Away Win or Draw")
    if y_pred < -1:
        print('Bet on a Away Win')
