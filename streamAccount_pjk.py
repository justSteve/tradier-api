import asyncio
import websockets

import argparse
from datetime import datetime
import os
import argparse
import config
import requests
import json
import sys
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import urllib
import logging
from sqlalchemy.exc import IntegrityError
from multiprocessing import Process, Manager, Lock
import json
import time

API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName = script_name


# Fetch session_id from the Tradier API
response = requests.post('https://api.tradier.com/v1/accounts/events/session',
                         data={},
                         headers={'Authorization': 'Bearer {}'.format(
                             config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
                         )
json_response = response.json()
session_id = json_response.get('stream', {}).get('sessionid', 'Default Value')
print(session_id)

lock = Lock()
def strToSQL(parsed_response):
    try:
    # Already parsed JSON response
        data_dict = parsed_response  
        print(f"Inside strToSQL, data_dict is: {data_dict}")

        # Validate that 'order' exists in data_dict
        if data_dict.get('event') == 'order':
            # Do something for 'order' events
            data_dict['source'] = tbleName  # Add a 'source' field to the dictionary
            df = pd.DataFrame([data_dict])  # Note that I wrapped data_dict in a list

            # Define the database connection string
            conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'
            
            # Create an SQLAlchemy engine
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
            
            try:
                # Write DataFrame to SQL table
                df.to_sql('AccountStream', engine, if_exists='append', index=False)
                logging.info(f"{tbleName}: Successfully got response from API with status code {response.status_code}")
            
            except IntegrityError as e:
                if '2627' in str(e.orig):  # Adjust the error code based on your database
                    print("Ignoring duplicate primary key.")
                else:
                    raise
            except Exception as e:
                logging.error(f"{tbleName}: Exception occurred: {e}")
                print("Error inserting data into SQL Server: ", e)
                raise
            else:
                print("The key 'order' is NOT found in data_dict.")
                
    except Exception as e:
        print(f"An error occurred: {e}")


async def connect_and_consume(shared_dict, lock):
    uri = "wss://ws.tradier.com/v1/accounts/events"
    tblName = "Positions"
    async with websockets.connect(uri) as websocket:
        payload_dict = {
            "events": ["order"],
            "sessionid": session_id,
            "excludeAccounts": []
        }
        payload_json = json.dumps(payload_dict)
        await websocket.send(payload_json)

        while True:
            try:
                response = await websocket.recv()
                parsed_response = json.loads(response)
                # Check if the event is not a heartbeat
                if parsed_response.get('event') != 'heartbeat':
                    strToSQL(parsed_response)
                    # Acquire lock before updating shared memory
                    with lock:
                        shared_dict['latest_data'] = parsed_response
                        

                print(f"< {response}")

            except Exception as e:
                print("exception hit!!")
                print(e)
                sys.exit(1)

# Wrapper function to run the asyncio loop


def run_asyncio_loop(shared_dict, lock):
    asyncio.run(connect_and_consume(shared_dict, lock))


def read_shared_memory(shared_dict, lock):
    while True:
        with lock:
            current_data = shared_dict.get('latest_data', {})
        print("Read from shared memory:", current_data)
        time.sleep(5)


if __name__ == "__main__":
    manager = Manager()
    shared_dict = manager.dict()

    # Process to update shared memory from WebSocket
    p1 = Process(target=run_asyncio_loop, args=(shared_dict, lock))

    # Process to read from shared memory
    p2 = Process(target=read_shared_memory, args=(shared_dict, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
