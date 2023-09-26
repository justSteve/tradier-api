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
logging.basicConfig(filename='tximport.log',
                    level=logging.INFO, format='%(asctime)s %(message)s')


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk

API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName = script_name


def importer(response):
    # Parse JSON string to a dictionary
    data_dict = response.json()

    # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict['order'])

    # Define the database connection string
    conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'

    # Connect to the database
    conn = pyodbc.connect(conn_str)

    # Create an SQLAlchemy engine
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")

    # Insert the data using to_sql
    try:
        df.to_sql('Orders', engine, index=False,
                  if_exists='append', method='multi', chunksize=500)

        logging.info(
            tbleName + ": Successfully got response from API with status code {response.status_code}")

    except Exception as e:

        logging.error(f"{tbleName}: Exception occurred: {e}")
        print("Error inserting data into SQL Server:", e)
        raise

    # Close the connection
    conn.close()


response = requests.get("https://api.tradier.com/v1/accounts/" + account_id + "/orders/" + id,
                        params={'includeTags': 'true'},
                        headers={"Authorization": "Bearer " +
                                 accessToken, "Accept": "application/json"}
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


importer(response)

print(response.status_code)
print(json_response)
print(account_id)
print(accessToken)


# CREATE TABLE Orders (
#     ID INT PRIMARY KEY IDENTITY(1,1),
#     api_id NVARCHAR(50),
#     type NVARCHAR(50),
#     symbol NVARCHAR(50),
#     side NVARCHAR(50),
#     quantity INT,
#     status NVARCHAR(50),
#     duration NVARCHAR(50),
#     price FLOAT,
#     avg_fill_price FLOAT,
#     exec_quantity INT,
#     last_fill_price FLOAT,
#     last_fill_quantity INT,
#     remaining_quantity INT,
#     create_date DATETIME,
#     transaction_date DATETIME,
#     class NVARCHAR(50),
#     option_symbol NVARCHAR(50),
#     stop_price FLOAT,
#     description NVARCHAR(255),
#     tag NVARCHAR(50),
#     source NVARCHAR(50) DEFAULT 'Tradier',
#     importDate DATETIME DEFAULT GETDATE()
# );
