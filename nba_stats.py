# imports
import streamlit as st
import pandas as pd
import numpy as np

st.title('NBA Player Stats Exploratory Data Analysis')
st.markdown("""
    This app web scrapes NBA player stats data.
    * **Data source:** [https://www.basketball-reference.com/](https://www.basketball-reference.com/)
    * **Python libraries:** streamlit, pandas, numpy 
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))

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

playerStats = load_data(selected_year)

