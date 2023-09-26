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
logging.basicConfig(filename='tximport.log', level=logging.INFO
                    , format='%(asctime)s %(message)s')


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk
API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName =script_name + '--GainLoss'

def get_params():
    params = {}
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Get Tradier API parameters.")
        parser.add_argument("--start", required=True, help="Start date")
        parser.add_argument("--end", required=True, help="End date")
        parser.add_argument("--page", default="0", help="Page number")
        parser.add_argument("--limit", default="50000", help="Limit")
        parser.add_argument("--sortBy", default="closeDate", help="Sort by")
        parser.add_argument("--sort", default="desc", help="Sort direction")
        parser.add_argument("--symbol", default="SPXW", help="Symbol")
        
        args = parser.parse_args()

        params["start"] = args.start
        params["end"] = args.end
        params["page"] = args.page
        params["limit"] = args.limit
        params["sortBy"] = args.sortBy
        params["sort"] = args.sort
        params["symbol"] = args.symbol
    else:
        params["start"] = "2023-09-18"
        params["end"] = "2023-09-19"
        params["page"] = "0"
        params["limit"] = "50000"
        params["sortBy"] = "closeDate"
        params["sort"] = "desc"
        params["symbol"] = "SPXW"
        
    return params

params = get_params()

def importGainLoss(response):
    logging.info("starting " + tbleName)
    # Parse JSON string to a dictionary
    data_dict = response.json()
    
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict['gainloss']['closed_position'])
    
    # Define the database connection string
    conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'
    
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    
    # Create an SQLAlchemy engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
    
    # Insert the data using to_sql
    try:
        df.to_sql('GainLoss', engine, index=False, if_exists='append', method='multi', chunksize=500)
        
        logging.info(tbleName + ": Successfully got response from API with status code {response.status_code}")
        
    except Exception as e:
        logging.error(f"{tbleName}: Exception occurred: {e}")
        print("Error inserting data into SQL Server:", e)
        raise
    
    # Close the connection
    conn.close()


try:
    response = requests.get(API_BASE_URL + "accounts/" + account_id + "/gainloss",
                        params=params,
                        headers={"Authorization": f"Bearer {accessToken}",
                                 "Accept": "application/json"})

    json_response = response.json()
    importGainLoss(response)

except Exception as e:
    
    logging.error(f"{tbleName}: Exception occurred: {e}")
    print (e)
    print(response)
    print(response.text)
    sys.exit(1)

print(response.status_code)
print(json_response)
print(account_id)
print(accessToken)


# CREATE TABLE GainLoss (
#     ID INT PRIMARY KEY IDENTITY(1,1),
#     close_date DATE,
#     cost FLOAT,
#     gain_loss FLOAT,
#     gain_loss_percent FLOAT,
#     open_date DATE,
#     proceeds FLOAT,
#     quantity INT,
#     symbol NVARCHAR(50),
#     term INT,
#     source NVARCHAR(50) DEFAULT 'Tradier',
#     importDate DATETIME DEFAULT GETDATE()
# );
