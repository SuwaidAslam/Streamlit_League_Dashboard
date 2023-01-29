import pandas as pd
import requests
import streamlit as st


#https://rapidapi.com/api-sports/api/api-football/              <- API Link
API_KEY = "6f5299c2b2mshc3faa0b885a77a5p1a3b0ejsn22871c9cb4f3"

HEADERS = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

@st.cache
def get_top_scorrers_players(season=2020):
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
    querystring = {"league":"39","season":season}
    response = requests.request("GET", url, headers=HEADERS, params=querystring)
    df = pd.json_normalize(response.json(), record_path=['response', 'statistics'],  meta=[['response', 'player', 'name'],
    ['response', 'player', 'age'], ['response', 'player', 'nationality']])
    return df

st.cache
def get_venues_map_data():
    url = "https://github.com/jokecamp/FootballData/blob/master/other/stadiums-with-GPS-coordinates.csv?raw=true"
    df = pd.read_csv(url, index_col=0)
    return df

st.cache
def get_attendence_byStadium():
    df = pd.read_csv('epl_stats.csv', usecols = ['date_GMT','attendance', 'stadium_name'],)
    return df

st.cache
def get_epl_standings_df():
    df = pd.read_csv('EPL Standings 2010-2021.csv')
    return df