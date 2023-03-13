import streamlit as st
import datetime
import requests
from app import *
from model_build.model_building import dl_model
from params import *

odds = get_odds()
game_dict = {}
for i in range(0,10):
    game_dict[f"game_{i+1}"] = f"{odds['HT'][i]} vs {odds['AT'][i]}"
game_list = list(game_dict.values())


response = requests.get(ODDS_API_URL).json()
datetime_dict = {}
next_games = response[:10]
for i in range(len(next_games)):
    datetime_dict[f"{odds['HT'][i]} vs {odds['AT'][i]}"] = (next_games[i]['commence_time'])


images_dict = {"Southampton":"https://icons.iconarchive.com/icons/giannis-zographos/british-football-club/256/Southampton-FC-icon.png",\
               "Tottenham":"https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Tottenham-Hotspur-icon.png",\
               'Bournemouth':"https://futhead.cursecdn.com/static/img/14/clubs/1943.png",\
               'Everton':'https://futhead.cursecdn.com/static/img/16/clubs/7.png',\
               'Leeds': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Leeds-United-icon.png',\
               'Leicester': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Leicester-City-icon.png',\
               'Crystal Palace': 'https://b.thumbs.redditmedia.com/P8rM4qw00rnLcgNG0rXORh0verHgaV3Ld1o3l-bRoBE.png',\
               'Fulham': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Fulham-FC-icon.png',\
               'West Ham': 'https://icons.iconarchive.com/icons/giannis-zographos/british-football-club/256/West-Ham-United-icon.png',\
               'Man United': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Manchester-United-icon.png',\
               'Newcastle': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Newcastle-United-icon.png',\
               'Liverpool': 'https://icons.iconarchive.com/icons/giannis-zographos/liverpool-fc/256/Liverpool-FC-icon.png',\
               'Brentford': 'https://b.thumbs.redditmedia.com/-59V1wKkxRjyq3Ja7XiyS5Z65NV4hcK0UoUe-OflcFM.png',\
               'Brighton': 'https://matchwornshirt.imgix.net/club/79/logo.png?auto=format,compress&w=256&h=256&fit=fit',\
               'Chelsea': 'https://www.iconarchive.com/download/i52558/giannis-zographos/english-football-club/Chelsea-FC.ico',\
               "Nott'm Forest": "https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Nottingham-Forest-icon.png",\
               'Man City': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Manchester-City-icon.png',\
               'Arsenal': "https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Arsenal-FC-icon.png",\
               'Aston Villa': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Aston-Villa-icon.png',\
               'Wolves': 'https://icons.iconarchive.com/icons/giannis-zographos/english-football-club/256/Wolverhampton-Wanderers-icon.png'}

stadium_dict = {"Southampton": "Saint Mary's Stadium",\
               "Tottenham": "Tottenham Hotspur Stadium",\
               'Bournemouth': "Dean Court",\
               'Everton': "Goodison Park",\
               'Leeds': "Elland Road",\
               'Leicester': "King Power Stadium",\
               'Crystal Palace': "Selhurst Park Stadium",\
               'Fulham': "Craven Cottage",\
               'West Ham': "London Stadium",\
               'Man United': "Old Trafford",\
               'Newcastle': "Saint James Park",\
               'Liverpool': "Anfield",\
               'Brentford': "Brentford Community Stadium",\
               'Brighton': "American Express Community Stadium",\
               'Chelsea': "Wembley Stadium",\
               "Nott'm Forest": "City Ground",\
               'Man City': "Etihad Stadium",\
               'Arsenal': "Emirates Stadium",\
               'Aston Villa': "Villa Park",\
               'Wolves': "Molineux Stadium"}



with st.form(key='params_for_api'):
    option = st.selectbox(
        'SELECT YOUR GAME',
        (game_list[0], game_list[1], game_list[2], game_list[3], game_list[4], game_list[5], game_list[6], game_list[7],\
            game_list[8], game_list[9]))
    if st.form_submit_button():
        st.write('You selected:', option)
        game = option.split(" vs ")
        home_team = game[0]
        away_team = game[1]

        date = str(datetime_dict[option]).split("T")
        day = date[0]
        time = date[1][:-4]
        stadium = stadium_dict[home_team]
        st.write(f'Game will be held at {stadium} on {day} at {time} !')

        model = dl_model()
        scaler = dl_scaler()
        X_new = get_x_new(home_team, away_team)
        X_new_processed = scaler.transform(X_new)
        y_pred = model.predict(X_new_processed)
        margin = y_pred[0]
        print(margin)
        if margin > 1:
            st.write('Bet on a Home Win')
            st.image(images_dict[home_team])
        if margin < 1 and margin > 0:
            st.write("Bet on a Home Win or Draw")
            st.image(images_dict[home_team])
        if margin > -1 and margin < 0:
            st.write("Bet on a Away Win or Draw")
            st.image(images_dict[away_team])
        if margin < -1:
            st.write('Bet on a Away Win')
            st.image(images_dict[away_team])
