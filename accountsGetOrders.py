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
import config_data
import config_logging


# Set up logging
config_logging.setup(__file__)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Script to process data based on account identifier.")
    parser.add_argument('-i', '--identifier', type=str, help='Account identifier e.g. sjh, pjk', default='pjk')
    return parser.parse_args()

args = get_args()
account_identifier = args.identifier

if account_identifier == 'pjk':
    account_id = config.ACCOUNT_ID_pjk
    accessToken = config.ACCESS_TOKEN_pjk
elif account_identifier == 'sjh':
    account_id = config.ACCOUNT_ID_sjh
    accessToken = config.ACCESS_TOKEN_sjh
else:
    print(f"Unsupported account identifier: {account_identifier}")
    exit(1)


API_BASE_URL = config.API_BASE_URL

# Extract the filename only
script_name = os.path.basename(__file__)

tbleName = script_name


def importer(response):
    if response.status_code != 200:
        logger.error(f"API call failed with status code: {response.status_code}")
        sys.exit(1)

    json_response = response.json()
    if 'orders' not in json_response or 'order' not in json_response['orders']:
        logger.error(f"Unexpected data structure: {json_response}")
        sys.exit(1)

    logging.debug(f"Type of json_response: {type(json_response)}")
    logging.debug(f"Content of json_response: {json_response}")


    # Parse JSON string to a dictionary
    data_dict = response.json()


    # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict['orders']['order'])

    # Insert the data
    try:
        config_data.insert_to_db(df, 'Orders')
        logging.info(f"Successfully got response from API with status code {response.status_code}")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        print("Error inserting data into SQL Server:", e)
        raise



response = requests.get("https://api.tradier.com/v1/accounts/" + account_id + "/orders",
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

try:
    importer(response)
except SystemExit as e:
    logger.error(f"Program exited with code {e.code}")


#print(response.status_code)
print(json_response)
#print(account_id)
#print(accessToken)

