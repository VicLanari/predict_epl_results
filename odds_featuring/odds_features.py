def get_odds_final(df):
    df_odds = df[["B365H", "B365D", "B365A", "BWH", "BWD", "BWA", "IWH", "IWD",\
    "IWA", "PSH", "PSD", "PSA", "WHH", "WHD", "WHA", "VCH", "VCD", "VCA",]]
    df_home_odds = df_odds[["B365H","BWH","IWH","WHH","VCH"]]
    df_home_odds["AHO"] = (df_home_odds["B365H"] + df_home_odds["BWH"] + df_home_odds["IWH"] + df_home_odds["WHH"] + df_home_odds["VCH"])/5


    df_away_odds = df_odds[["B365A","BWA","IWA","WHA","VCA"]]
    df_away_odds["AAO"] = (df_away_odds["B365A"] + df_away_odds["BWA"] + df_away_odds["IWA"] + df_away_odds["WHA"] + df_away_odds["VCA"])/5
    df_odds_final = df_home_odds[["AHO"]]
    df_odds_final = df_odds_final.join(df_away_odds[["AAO"]])
    return df_odds_final
