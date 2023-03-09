from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import pandas as pd
from sklearn.preprocessing import RobustScaler
from import_pack.import_data import *
from odds_featuring.odds_features import get_odds_final
from stats_pack.stats_features import stats_features
from cloud_interaction.upload import upload_model
import os
import pickle

BUCKET_NAME = os.environ.get("BUCKET_NAME")

def data_prepare_for_split(df):
    df_odds = get_odds_final(df)
    df_stats = stats_features(df)
    df_final = df_stats.join(df_odds)
    df_final['Date'] = pd.to_datetime(df['Date'])
    df_final.dropna(inplace=True)
    return df_final

def preprocess(X_train, X_test):
    scaler = RobustScaler()
    X_train_processed = scaler.fit_transform(X_train)
    X_test_processed = scaler.transform(X_test)
    return X_train_processed, X_test_processed

def tt_split(df):
    X_train = df.loc[df['Date'] < '2021/01/01']
    X_test = df.loc[df['Date'] >= '2021/01/01']
    y_train = df['margin'].loc[df['Date'] < '2021/01/01']
    y_test = df['margin'].loc[df['Date'] >= '2021/01/01']
    X_train.drop(columns=['Date', 'margin'], inplace=True)
    X_test.drop(columns=['Date', 'margin'], inplace=True)
    return X_train, X_test, y_train, y_test

def initialize_model():
    model = LinearRegression()
    return model

def train_model(model, X_train_processed, y_train):
    model = model.fit(X_train_processed, y_train)
    upload_model(model)
    return model

def check_conditions(margin, prediction):
    output = 0
    if margin == 0:
        if prediction < 1 and prediction > -1:
            output = 1
    if margin > 0:
        if prediction > 0:
            output = 1
    if margin < 0:
        if prediction < 0:
            output = 1
    return output

def evaluate(model, X_test_processed, y_test):
    r2 = model.score(X_test_processed, y_test)
    y_pred = model.predict(X_test_processed)
    mae = mean_absolute_error(y_test, y_pred)
    y_test = pd.DataFrame(y_test).reset_index(drop=True)
    y_pred = pd.DataFrame(y_pred).reset_index(drop=True)
    y_compare = y_test.join(y_pred)
    y_compare = y_compare.rename(columns={0:'prediction'})
    y_compare['correct'] = y_compare.apply(lambda x: check_conditions(x['margin'], x['prediction']), axis=1)
    ratio = y_compare['correct'].value_counts(normalize=True)
    return r2, mae, ratio

def dl_model():
    from google.cloud import storage
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="models"))
    blob = blobs[-1]
    pickle_in = blob.download_as_string()
    model = pickle.loads(pickle_in)
    print("✅ Model loaded from gcs")
    return model


# if __name__ == '__main__':
#     dl_model()
