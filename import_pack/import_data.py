import pandas as pd

LINKS = ["mmz4281/2223/E0.csv",
 "mmz4281/2122/E0.csv",
 "mmz4281/2021/E0.csv",
 "mmz4281/1920/E0.csv",
 "mmz4281/1819/E0.csv",
 "mmz4281/1718/E0.csv",
 "mmz4281/1617/E0.csv",
 "mmz4281/1516/E0.csv",
 "mmz4281/1415/E0.csv",
 "mmz4281/1314/E0.csv",
 "mmz4281/1213/E0.csv",
 "mmz4281/1112/E0.csv",
 "mmz4281/1011/E0.csv",
 "mmz4281/0910/E0.csv",
 "mmz4281/0809/E0.csv",
 "mmz4281/0708/E0.csv",
 "mmz4281/0607/E0.csv",
 "mmz4281/0506/E0.csv"]


def grab_epl_data():
    df = pd.DataFrame()
    for link in LINKS:
        # print(f"https://www.football-data.co.uk/{link}")
        df = pd.concat([df, pd.read_csv(f"https://www.football-data.co.uk/{link}")])
    return df

def split_data(df):
    results_col = ['Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
       'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee']
    stats_col = ['HS', 'AS', 'HST', 'AST','HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    odds_col = ['B365H', 'B365D',\
       'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD',\
       'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'MaxH', 'MaxD',\
       'MaxA', 'AvgH', 'AvgD', 'AvgA', 'B365>2.5', 'B365<2.5', 'P>2.5',\
       'P<2.5', 'Max>2.5', 'Max<2.5', 'Avg>2.5', 'Avg<2.5', 'AHh',\
       'B365AHH', 'B365AHA', 'PAHH', 'PAHA', 'MaxAHH', 'MaxAHA', 'AvgAHH',\
       'AvgAHA', 'B365CH', 'B365CD', 'B365CA', 'BWCH', 'BWCD', 'BWCA',\
       'IWCH', 'IWCD', 'IWCA', 'PSCH', 'PSCD', 'PSCA', 'WHCH', 'WHCD',\
       'WHCA', 'VCCH', 'VCCD', 'VCCA', 'MaxCH', 'MaxCD', 'MaxCA', 'AvgCH',\
       'AvgCD', 'AvgCA', 'B365C>2.5', 'B365C<2.5', 'PC>2.5', 'PC<2.5',\
       'MaxC>2.5', 'MaxC<2.5', 'AvgC>2.5', 'AvgC<2.5', 'AHCh', 'B365CAHH',\
       'B365CAHA', 'PCAHH', 'PCAHA', 'MaxCAHH', 'MaxCAHA', 'AvgCAHH',\
       'AvgCAHA', 'Bb1X2', 'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA',\
       'BbAvA', 'BbOU', 'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5',\
       'BbAH', 'BbAHh', 'BbMxAHH', 'BbAvAHH', 'BbMxAHA', 'BbAvAHA', 'LBH',\
       'LBD', 'LBA', 'SJH', 'SJD', 'SJA', 'GBH', 'GBD', 'GBA', 'BSH',\
       'BSD', 'BSA', 'SBH', 'SBD', 'SBA']
    df_results = df[results_col]
    df_stats = df[stats_col]
    df_odds = df[odds_col]
    return df_results, df_stats, df_odds


if __name__ == '__main__':
    df = grab_epl_data()
    df_results, df_stats, df_odds = split_data(df)
