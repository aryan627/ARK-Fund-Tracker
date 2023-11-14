import psycopg2 
import psycopg2.extras
import config
import pandas as pd
from datetime import date
import streamlit as st
import numpy as np

connection = psycopg2.connect(host=config.DB_HOST,database=config.DB_NAME,user=config.DB_USER, password= config.DB_PASS) 
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""
    select * from etf_holding order by etf_id, holding_id, dt;
""")
records = cursor.fetchall() 
df = pd.DataFrame(records,columns=['etf_id','holding_id','dt_date','shares','weight']).sort_values(['etf_id','holding_id'],ascending=True)
def make_clickable(x):
# target _blank to open new window
    return f"<a target='_blank' href='https://finviz.com/chart.ashx?t={x}'>{x}</a>"

def share_differences(df1,df2,name):

    holding_differences = pd.DataFrame()
    holding_differences= pd.merge(df2,df1,on='holding_id',how='outer')
    holding_differences['diff'] = holding_differences['shares_x']-holding_differences['shares_y'] 
    holding_differences['wdiff'] = holding_differences['weight_x']-holding_differences['weight_y'] 


    global updates
    updates = pd.DataFrame(columns=('ETF','Removed/Added', 'Shares Difference','Weight Difference','Stock Ticker'))
    for row in holding_differences.iterrows():
        sharesd = ((row[1]['diff']))
        id_value = ((row[1]['holding_id']))
        weightd = ((row[1]['wdiff']))
        if sharesd != 0 :
            cursor.execute("""
                select name,symbol from stock where id = %s
            """,(int(id_value),))
            stock_name = cursor.fetchone()
            if sharesd < 0:
                row = [name,'Removed',sharesd,weightd,stock_name[1]]
                updates.loc[len(updates)] = row
            else:
                row = [name,'Added',sharesd,weightd,stock_name[1]]
                updates.loc[len(updates)] = row   

    
    st.subheader('Updates')
    st.write(updates)
    

def differences(name):
    st.header(f'{name} HOLDINGS')
    cursor.execute("""
    select id from stock where is_etf = true and symbol = %s
""",(name,))
    etf_id = cursor.fetchone()

    mask = df["etf_id"] == etf_id[0]
    etf_holdings = df[mask]

    dates = etf_holdings['dt_date'].unique()

    def later_date(l):
        if l[0]>l[1]:
            return l[0]
        else:
            return l[1]
    date_mask = etf_holdings['dt_date'] == later_date(dates)
    df1 = etf_holdings[~date_mask].reset_index(drop=True)
    df2 = etf_holdings[date_mask].reset_index(drop=True)


    
    previous_holding_ids = df1['holding_id'].unique()
    current_holding_ids = df2['holding_id'].unique()


    added_stocks=(set(current_holding_ids)-set(previous_holding_ids))
    removed_stocks = (set(previous_holding_ids)-set(current_holding_ids))




    if not added_stocks or not removed_stocks:
        share_differences(df1,df2,name)
    else:
        for stock_id in added_stocks:
            cursor.execute("""
                select name,symbol from stock where id = %s
            """,(int(stock_id),))
        
            stock_name = cursor.fetchone()
            st.subheader(f'{name} ETF ADDED ${stock_name[1]} to the ETF')
            st.image(f'https://finviz.com/chart.ashx?t={stock_name[1]}')

        for stock_id in removed_stocks:
            cursor.execute("""
                select name,symbol from stock where id = %s
            """,(int(stock_id),))
            stock_name = cursor.fetchone()
            st.subheader(f'{name} ETF REMOVED ${stock_name[1]} from the ETF')
            st.image(f'https://finviz.com/chart.ashx?t={stock_name[1]}')

        share_differences(df1,df2,name)

    def find_ticker(x):
        cursor.execute("""
            select symbol from stock where id = %s
        """,(int(str(x)),))
        stock = cursor.fetchone()
        return stock[0]
    
    df1['Stock Ticker'] = df1['holding_id'].apply(find_ticker)
    df1['Stock Ticker'] = df1['Stock Ticker'].apply(make_clickable)
    df1 = df1.to_html(escape=False)
    df2['Stock Ticker'] = df2['holding_id'].apply(find_ticker)
    df2['Stock Ticker'] = df2['Stock Ticker'].apply(make_clickable)
    df2 = df2.to_html(escape=False)
    with st.beta_expander("Previous Holdings"):
        st.write(df1,unsafe_allow_html=True)
    with st.beta_expander("Current Holdings"):
        st.write(df2,unsafe_allow_html=True)


def most_removed():
    f = updates.fillna(0)
    f['Shares Difference']=f['Shares Difference'].astype(int)
    return f.nsmallest(5,"Shares Difference")

def most_added():
    f = updates
    f['Shares Difference']=f['Shares Difference'].astype(int)
    return f.nlargest(5,"Shares Difference")


def most_removedw():
    f = updates.fillna(0)
    f['Weight Difference']=f['Weight Difference'].astype(float)
    return f.nsmallest(5,"Weight Difference")

def most_addedw():
    f = updates
    f['Weight Difference']=f['Weight Difference'].astype(float)
    return f.nlargest(5,"Weight Difference")