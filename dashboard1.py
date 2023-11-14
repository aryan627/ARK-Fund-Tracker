# import psycopg2 
# import psycopg2.extras
import config
import pandas as pd
from datetime import date
import streamlit as st
import numpy as np
# from helpers import differences
# from helpers import share_differences
# from helpers import most_removed
# from helpers import most_added
# from helpers import most_removedw
# from helpers import most_addedw
c_date = (date.today())

# connection = psycopg2.connect(host=config.DB_HOST,database=config.DB_NAME,user=config.DB_USER, password= config.DB_PASS) 
# cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

option = st.sidebar.selectbox("Which  ARK ETF?", ('ARKF','ARKG','ARKK','ARKQ','ARKW'))


if option=='ARKF':
    # differences('ARKF')
    st.write("ARKF")
if option == 'ARKG':
    # differences('ARKG')
    st.write("ARKF")
if option=='ARKQ':
    st.write("ARKF")
    # differences('ARKQ')
if option == 'ARKW':
    st.write("ARKF")
    # differences('ARKW')
if option == 'ARKK':
    st.write("ARKF")
    # differences('ARKW')

functions = st.sidebar.selectbox("Which Filter?",("5 Most Removed by Shares","5 Most Added by Shares","5 Most Removed by Weight","5 Most Added by Weight","None"),)
if functions == '5 Most Removed by Shares':
    st.subheader('5 Most Removed Holdings by Shares')
    # st.write(most_removed())
if functions == '5 Most Added by Shares':
    st.subheader('5 Most Added Holdings by Shares')
    # st.write(most_added())
if functions == '5 Most Removed by Weight':
    st.subheader('5 Most Removed Holdings by Weight')
    chart_data = pd.DataFrame(np.random.randn(20, 5), columns=["AAPL", "TSLA", "COIN", "ROKU", "SQ"])

    st.bar_chart(chart_data)
    # st.write(most_removedw())
if functions == '5 Most Added by Weight':
    st.subheader('5 Most Added Holdings by Weight')
    # st.write(most_addedw())
if functions == "None":
    st.write(" ")


darkmode = """
<style>
body {
  background-color: black;
  color: white;
}
</style>
"""

buffer = st.sidebar.checkbox('Dark Mode')
if buffer:
    st.markdown(darkmode,unsafe_allow_html=True)





















