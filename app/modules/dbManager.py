import sqlite3
import streamlit as st
import pandas as pd
import requests
import time

def query(query, data, type):
    try:
        conn = sqlite3.connect('app\\data\\spaceTradersV2.db')
        cur = conn.cursor()
        
        resCurs = cur.execute(query, data)

        if type == "write":
            conn.commit()
        else: 
            result = resCurs.fetchall()
            return result

        cur.close()
    except sqlite3.Error as error:
        st.write("Failed to insert data into sqlite table", error)
    finally:
        conn.close()

def insertTraits(data):
    df_traits = pd.json_normalize(data, record_path = ['traits'], errors="ignore")

    conn = sqlite3.connect('app\\data\\spaceTradersV2.db')

    df_traits.to_sql(name="Traits", con=conn, if_exists="append", index=False)

    conn.close() 

    for trait in data['traits']:
        res = query(f'select trait_id from Traits where symbol = (?)', [trait['symbol']], 'read')

        query(f'insert into WaypointTraits (waypoint_symbol, trait_id) VALUES ((?), (?))', [data['symbol'], res[0][0]], 'write')


def insertContracts(data, agentName, method):
    conn = sqlite3.connect('app\\data\\spaceTradersV2.db')

    df_main = pd.json_normalize(data)

    res = query('select accountId from Agent where symbol = (?)', [agentName], 'read')
 
    df_main.insert(1, 'agent', res[0][0], True)
    df_main = df_main.rename(columns={'terms.deadline' : 'deadline', 'terms.payment.onAccepted' : 'onAccept', 'terms.payment.onFulfilled': 'onFulfilled'})

    df_main = df_main.drop(columns='terms.deliver')

    df_main.to_sql(name='Contracts', con=conn, if_exists=method, index=False)

    df_deliver = pd.json_normalize(data, record_path= ['terms', 'deliver'])
    df_deliver.insert(1, 'contractId', df_main['id'], True)

    df_deliver.to_sql(name='ContractDeliverables', con=conn, if_exists=method, index=False)

    conn.close()


def systemTablePopulate():
    conn = sqlite3.connect('app\\data\\spaceTradersV2.db')

    for page in range(1, 425):
        params = {
            'limit': 20,
            'page': page
        }
        
        response = requests.get('https://api.spacetraders.io/v2/systems', headers=st.session_state['headers'], params=params).json()


        df = pd.json_normalize(response['data'])

        df_factions = pd.json_normalize(response['data'], record_path = 'factions', record_prefix = 'factions', meta = ['symbol'])
        df_factions = df_factions.rename(columns={'factionssymbol' : 'faction_symbol', 'symbol' : 'system_symbol'})

        df = df.drop(columns='waypoints')
        df = df.drop(columns='factions')

        df = df.rename(columns={'sectorSymbol' : 'sector_symbol'})

        df.to_sql(con=conn, name='Systems', if_exists='append', index=False)
        df_factions.to_sql(con=conn, name='SystemFactions', if_exists='append', index=False)

        time.sleep(1)

    conn.close()
    

def populateWaypointsTable():
    try:
        conn = sqlite3.connect('app\\data\\spaceTradersV2.db')
        cur = conn.cursor()
        
        resCurs = cur.execute('select symbol from Systems;')

        result = resCurs.fetchall()
        
        for system in result:
            response = requests.get(f'https://api.spacetraders.io/v2/systems/{system[0]}', headers=st.session_state['headers']).json()

            print(response['data']['symbol'])

            df = pd.json_normalize(response['data']['waypoints'])
            if 'orbitals' in df.columns:
                df = df.drop(columns=['orbitals'])

            df['system_symbol'] = response['data']['symbol']

            df.to_sql(con=conn, name='Waypoints', if_exists='append', index=False)


            for waypoint in response['data']['waypoints']:
                if waypoint['orbitals']:
                    df2 = pd.DataFrame(waypoint['orbitals'])
                    df2['waypoint_symbol'] = waypoint['symbol']

                    df2.to_sql(con=conn, name='WaypointOrbitals', if_exists='append', index=False)

            time.sleep(1)

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        conn.close()
    

