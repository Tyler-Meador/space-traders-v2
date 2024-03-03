import sqlite3
import streamlit as st
import pandas as pd

def query(query, data, type):
    try:
        conn = sqlite3.connect('app\\data\\spaceTradersV2.db')
        cur = conn.cursor()
        
        resCurs = cur.execute(query, data)

        if type == "write":
            res = conn.commit()
            st.write(res)
        else: 
            result = resCurs.fetchall()
            return result

        cur.close()
    except sqlite3.Error as error:
        st.write("Failed to insert data into sqlite table", error)
    finally:
        conn.close()

def insertWaypoints(data):

    df_main = pd.json_normalize(data)



    df_traits = pd.json_normalize(data, record_path = ['traits'], record_prefix='traits.', meta='symbol', errors="ignore")

    df_orbitals = pd.json_normalize(data, record_path = ['orbitals'], record_prefix='orbitals.', meta='symbol')

    df_out = (df_main.merge(df_traits, on = 'symbol', how='left')
            .merge(df_orbitals, on = "symbol", how='left')
            .drop(['traits', 'orbitals'], axis=1))

    df_out = df_out.mask(df_out.map(type).eq(list) & ~df_out.astype(bool))

    conn = sqlite3.connect('app\\data\\spaceTradersV2.db')

    df_out.to_sql(name="waypoints", con=conn, if_exists="replace", index=False)

    conn.close()

def insertContracts(data, agent):
    conn = sqlite3.connect('app\\data\\spaceTradersV2.db')

    df_main = pd.json_normalize(data)
    df_main.insert(1, 'agent', agent, True)

    df_deliver = pd.json_normalize(data, record_path= ['terms', 'deliver'], record_prefix='terms.deliver.', meta='id')

    df_out = df_main.merge(df_deliver, on = 'id').drop('terms.deliver', axis=1)

    df_out.to_sql(name="contracts", con=conn, if_exists="append", index=False)

    conn.close()