import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import urllib
import logging

logger = logging.getLogger(__name__)

# Constants or configuration data
CONN_STR = r'DRIVER={ODBC Driver 17 for SQL Server};Server=(LocalDB)\MSSQLLocalDB;Database=OptionsTracking;Integrated Security=True;'

def get_engine():
    """Create and return a SQLAlchemy engine."""
    return create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(CONN_STR)}")

def insert_to_db(df: pd.DataFrame, table_name: str):
    """Insert data from DataFrame into specified table."""
    try:
        with get_engine().connect() as connection:
            df.to_sql(table_name, connection, index=False,
                      if_exists='append', method='multi', chunksize=500)
            logger.info(f"Successfully inserted data into {table_name}")
    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}")
        raise
