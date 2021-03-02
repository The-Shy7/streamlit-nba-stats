# imports
import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import ssl

# workaround of SSL certificate verification 
# failure bug on MacOS and Python 3
# https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3
ssl._create_default_https_context = ssl._create_unverified_context

st.title('NBA Player Stats Exploratory Data Analysis')
st.markdown("""
    This app web scrapes NBA player stats data.
    * **Data source:** [https://www.basketball-reference.com/](https://www.basketball-reference.com/)
    * **Python libraries:** streamlit, pandas, numpy, base64, seaborn, matplotlib
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

# heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Heatmap')
    # tried creating heatmap from df_selected_team, but didn't work
    # worked when exporting it out as a file and reading it back in
    df_selected_team.to_csv('output.csv', index = False)
    df = pd.read_csv('output.csv')
    
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize = (7, 5))
        ax = sns.heatmap(corr, mask = mask, vmax = 1, square = True)
    st.pyplot(f)
    