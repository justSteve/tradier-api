
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
from pandas import json_normalize

logging.basicConfig(filename='tximport.log',
                    level=logging.INFO, format='%(asctime)s %(message)s')


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk

API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName = script_name + '--History'

# accountsHistory_pjk.py


def create_params(cli_args=None):
    params = {}

    if cli_args:
        if cli_args.page:
            params['page'] = cli_args.page
        if cli_args.limit:
            params['limit'] = cli_args.limit
        if cli_args.type:
            params['type'] = cli_args.type
        if cli_args.start:
            params['start'] = cli_args.start
        if cli_args.end:
            params['end'] = cli_args.end
        if cli_args.symbol:
            params['symbol'] = cli_args.symbol
        if cli_args.exactMatch:
            params['exactMatch'] = cli_args.exactMatch
    else:
        # Static parameters when no CLI args are provided
        params = {
            'page': '3',
            'limit': '100',
            'type': 'trade,option,ach,wire,dividend,fee,tax,journal,check,transfer,adjustment,interest',
            'start': 'yyyy-mm-dd',
            'end': 'yyyy-mm-dd',
            'symbol': 'SPY',
            'exactMatch': 'true'
        }

    return params


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Generate account history parameters')
    parser.add_argument('--page', help='Page number')
    parser.add_argument('--limit', help='Limit number of entries')
    parser.add_argument('--type', help='Type of transactions')
    parser.add_argument('--start', help='Start date (yyyy-mm-dd)')
    parser.add_argument('--end', help='End date (yyyy-mm-dd)')
    parser.add_argument('--symbol', help='Symbol like SPY')
    parser.add_argument(
        '--exactMatch', help='Whether to perform an exact match (true/false)')

    return parser.parse_args()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_args = parse_cli_args()
        params = create_params(cli_args)
    else:
        params = create_params()

    print("Generated parameters:", params)


def importer(response):

    # Parse JSON string to a dictionary
    data_dict = response.json()
    
    # Flatten the nested structure
    flattened_data = json_normalize(data_dict['history']['event'])

    # Convert dictionary to DataFrame
    df = pd.DataFrame(flattened_data)
    
    # Define the database connection string
    conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'
    
    # Create an SQLAlchemy engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
    
    try:
    # Write DataFrame to SQL table
        
        df.to_sql('History', engine, if_exists='append', index=False)
        
        logging.info(
            tbleName + ": Successfully got response from API with status code {response.status_code}")

    except Exception as e:

        logging.error(f"{tbleName}: Exception occurred: {e}")
        print("Error inserting data into SQL Server:", e)
        raise

    # Close the connection conn_str.close()


response = requests.get("https://api.tradier.com/v1/accounts/" + account_id + "/history",
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

