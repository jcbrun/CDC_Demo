from google.cloud import bigquery
from google.oauth2 import service_account
from time import sleep

if __name__ == '__main__':
    # Construct a BigQuery client object.
    credentials = service_account.Credentials.from_service_account_file( '/home/jcbrun/SA-Key/ambient-antenna-369806-3bb882e508c4.json')
    project_id = 'ambient-antenna-369806'
    client = bigquery.Client(credentials= credentials,project=project_id)
    table_id = "ambient-antenna-369806.dataDemo.cdc_log_personne"


    sql_createTable = """
    CREATE OR REPLACE TABLE `{}` (
	    op STRING,
	    ts_ms INT64,
	    id INT64,
	    first_name STRING,
	    last_name STRING,
	    email STRING
        )
    OPTIONS(
        description="log cdc",
        labels=[("cdc", "debezium")]
    );
    """.format( table_id)

    job = client.query(sql_createTable)  # API request.
    job.result()  # Waits for the query to finish.


    print(
        'Created new view "{}.{}.{}".'.format(
            job.destination.project,
            job.destination.dataset_id,
            job.destination.table_id,
        )
    )
    
