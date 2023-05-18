import snowflake.connector
from time import sleep
import os

PASSWORD=os.getenv("SNOW_PASSWORD")

if __name__ == '__main__':
    # Construct a Snowflake client object.
    conn = snowflake.connector.connect(
        user='jcbrun',
        password=PASSWORD,
        account='kq07505.europe-west4.gcp',
        database='MA_DEMO'
    )
    
    table_id = 'public.cdc_log_personne'
    sql_createTable = """
        CREATE OR REPLACE TABLE {} (
            op STRING,
            ts_ms INT,
            id INT,
            first_name STRING,
            last_name STRING,
            email STRING
        );
        """.format(table_id)
        
    try:
        # Running queries
        conn.cursor().execute(sql_createTable)
    finally:
        # Closing the connection
        conn.close()
    
    
