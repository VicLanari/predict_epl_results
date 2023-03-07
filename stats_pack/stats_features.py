def stats_features(df):
    stat_cols = ['AC', 'AF', 'AR', 'AS', 'AST', 'AY', 'HC', 'HF', 'HR', 'HS', 'HST', 'HY', 'margin']
    df['margin'] = df['FTHG'] - df['FTAG']
    df_stats = df[stat_cols]
    df_stats['THC'] = df_stats['HY'] + df_stats['HR']
    df_stats['TAC'] = df_stats['AY'] + df_stats['AR']
    final_cols = ['AST', 'HST', 'HC', 'AC', 'THC', 'TAC', 'margin']
    df_final = df_stats[final_cols]
    return df_final
