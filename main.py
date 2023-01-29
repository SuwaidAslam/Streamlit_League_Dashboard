"""Main module for the streamlit app"""
import numpy as np
import pandas as pd
import streamlit as st
from api import *
import plotly.express as px
import folium
from streamlit_folium import st_folium
from plotly import graph_objects as go



# Config the whole app
st.set_page_config(
    page_title="Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.sidebar.title('Navigation')
    pages = ['Home']
    page = st.sidebar.radio(
    "Go to", pages,
    horizontal=True,
    )
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    if page == pages[0]:
        column_names = {
        'Games Apearances' : 'games.appearences',
        'Games Minutes' : 'games.minutes',
        'Dribbles Success' : 'dribbles.success',
        'Total Goals' : 'goals.total'
        }
        _, center_col, _ = st.sidebar.columns([1,1,1])
        with center_col:
            st.button('Controlls', disabled=True)
        st.sidebar.info('Filter Graphs and Table Using Contolls Bellow', icon="ℹ️")
        agree = st.sidebar.checkbox('Like to Change Background?')
        if agree:
            color = st.sidebar.color_picker('Pick an App Background Color', '#100E0E')  
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-color : {color}
                }}
                </style>
                """,
                unsafe_allow_html=True
                )

        season = st.sidebar.number_input("Filter By Season", min_value=2017, max_value=2022)

        players_df = get_top_scorrers_players(season)
        option = st.sidebar.selectbox(
            'Filter Players By',
            list(column_names))
        players_df = players_df.nlargest(10, column_names.get(option))

        # table and Bar chart
        st.markdown(f"<h2 style='text-align: center;'>Top 10 Players By {option}</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            players_df_table = players_df[['response.player.name', 'response.player.age', 'response.player.nationality', 'team.name']]
            players_df_table = players_df_table.set_axis(['Name', 'Age', 'Nationality', 'Team Name'], axis=1)
            players_df_table = players_df_table.reset_index(drop=True)
            st.dataframe(players_df_table, use_container_width=True)
        with col2:
            fig = px.bar(players_df, x='response.player.name', y=column_names.get(option), color='response.player.name')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            # map graph
            map_df = get_venues_map_data()
            map_df = map_df.nlargest(20, 'Capacity')
            map = folium.Map(location=[map_df.Latitude.mean(), 
            map_df.Longitude.mean()],
            zoom_start=5, control_scale=True)
            for index, location_info in map_df.iterrows():
                folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=location_info["Stadium"]).add_to(map)
            
            st.markdown(f"<h2 style='text-align: center;'>20 Largest Stadiums By Capacity</h2>", unsafe_allow_html=True)
            st_folium(map, width=1000, height=500)

        with col4:
            st.markdown(f"<h2 style='text-align: center;'>Attendance By Stadium</h2>", unsafe_allow_html=True)
            attendence_df = get_attendence_byStadium()
            line_fig = px.area(attendence_df, x="date_GMT", y="attendance", color='stadium_name')
            line_fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, showlegend=False)
            st.plotly_chart(line_fig, use_container_width=True)
        

        # Multiseason bar charts
        epl_std_df = get_epl_standings_df()
        seasons = epl_std_df['Season'].unique()
        multi_seasons = st.multiselect(label="Choose Multiple Seasons",
            options=seasons, default=seasons[0])

        for s in multi_seasons:
            filtered_season = epl_std_df[epl_std_df['Season'] == s]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=filtered_season['Team'],
                y=filtered_season['Pld'],
                name='Matches played',
                marker_color='mediumvioletred'
            ))
            fig.add_trace(go.Bar(
                x=filtered_season['Team'],
                y=filtered_season['W'],
                name='Matches win',
                marker_color='springgreen'
            ))
            fig.add_trace(go.Bar(
                x=filtered_season['Team'],
                y=filtered_season['D'],
                name='Matches draw',
                marker_color='dodgerblue'
            ))
            fig.add_trace(go.Bar(
                x=filtered_season['Team'],
                y=filtered_season['L'],
                name='Matches loss',
                marker_color='darkblue'
            ))

            fig.update_layout(title=f"Matches Played-Win-Draw-Loss In Season {s}",
                            barmode='stack',
                            title_font_size=30,
                            xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        st.sidebar.success('Dashboard Loaded!', icon="✅")
    


if __name__ == "__main__":
    main()
