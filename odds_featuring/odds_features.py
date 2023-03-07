def get_odds_final(df):
    df_odds = df[["B365H", "B365D", "B365A", "BWH", "BWD", "BWA", "IWH", "IWD",\
    "IWA", "PSH", "PSD", "PSA", "WHH", "WHD", "WHA", "VCH", "VCD", "VCA",]]
    df_odds["AHO"] = (df_odds["B365H"] + df_odds["BWH"] + df_odds["IWH"] + df_odds["WHH"] + df_odds["VCH"])/5
    df_odds["AAO"] = (df_odds["B365A"] + df_odds["BWA"] + df_odds["IWA"] + df_odds["WHA"] + df_odds["VCA"])/5
    print(df_odds.shape, df_odds.shape)
    df_odds = df_odds[["AAO", "AHO"]]
    print(df_odds.shape)
    return df_odds
