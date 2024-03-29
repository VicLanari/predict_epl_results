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

r2, mae, ratio = evaluate(model, X_test_processed, y_test)
