# imports
import streamlit as st
import pandas as pd
import numpy as np
import base64

st.title('NBA Player Stats Exploratory Data Analysis')
st.markdown("""
    This app web scrapes NBA player stats data.
    * **Data source:** [https://www.basketball-reference.com/](https://www.basketball-reference.com/)
    * **Python libraries:** streamlit, pandas, numpy 
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2021))))

# web scrape nba player stats from basketball-reference
@st.cache # function will be cached
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # deletes repeating headers in the content
    raw = raw.fillna(0)
    playerStats = raw.drop(['Rk'], axis = 1) # redundant with index provided by pandas
    return playerStats

# retrieves nba player stats from the selected 
# year provided by the user
playerStats = load_data(selected_year) 

# team selection from sidebar
sorted_unique_team = sorted(playerStats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# position selection from sidebar
positions = ['C', 'PF', 'SF', 'PG', 'SG']
selected_position = st.sidebar.multiselect('Position', positions, positions)

# filter data
df_selected_team = playerStats[(playerStats.Tm.isin(selected_team)) & (playerStats.Pos.isin(selected_position))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)