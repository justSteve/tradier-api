
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

logging.basicConfig(filename='tximport.log',
                    level=logging.INFO, format='%(asctime)s %(message)s')


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk

API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName = script_name

# accountsPositions_pjk.py


def importer(response):

    # Parse JSON string to a dictionary
    data_dict = response.json()

    # Adding a new field to each dictionary in the list
    for item in data_dict['positions']['position']:
        item['source'] = tbleName  # Replace 'new_field' and 'new_value' with what you need

    
    # Flatten the nested structure flattened_data = json_normalize(data_dict['positions']['position'])

    # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict['positions']['position'])
    
    # Define the database connection string
    conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'
    
    # Create an SQLAlchemy engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
    
    try:
    # Write DataFrame to SQL table
        
        df.to_sql('Positions', engine, if_exists='append', index=False)
        
        logging.info(
            tbleName + ": Successfully got response from API with status code {response.status_code}")
    except IntegrityError as e:
        # Assuming error code for duplicate primary key is 2627 for SQL Server
        if '3621' in str(e.orig):
            print("Ignoring duplicate primary key.")
        else:
            raise
    except Exception as e:

        logging.error(f"{tbleName}: Exception occurred: {e}")
        print("Error inserting data into SQL Server:", e)
        raise

    # Close the connection conn_str.close()


response = requests.get(API_BASE_URL + "accounts/" + account_id + "/positions",
                        params={},
                        headers={"Authorization": "Bearer " +
                                 accessToken , "Accept": "application/json"}
                        )
try:
    json_response = response.json()

except Exception as e:

    logging.error(f"{tbleName}: Exception occurred: {e}")
    print("exception hit!!")
    print(e)
    print(response)
    print(response.text)
    sys.exit(1)

# Check if request was successful
if response.status_code >= 200 and response.status_code < 300:
    json_data = response.json()

    # Check if json_data is None
    if json_data['positions'] is None:
        print("JSON data is None")
    else:
        print("JSON data is not None")
        importer(response)

print(response.status_code)
print(json_response)
print(account_id)
print(accessToken)

# CREATE TABLE [dbo].[History](
# 	[amount] [float] NULL,
# 	[date] [varchar](max) NULL,
# 	[type] [varchar](max) NULL,
# 	[trade.commission] [float] NULL,
# 	[trade.description] [varchar](max) NULL,
# 	[trade.price] [float] NULL,
# 	[trade.quantity] [float] NULL,
# 	[trade.symbol] [varchar](max) NULL,
# 	[trade.trade_type] [varchar](max) NULL
# ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
# GO

