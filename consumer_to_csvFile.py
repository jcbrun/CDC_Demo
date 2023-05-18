import json
from kafka import KafkaConsumer
from datetime import datetime
import pytz
from time import sleep
from deepdiff import DeepDiff

print("Waiting on Messages ...")
if __name__ == '__main__':
    consumer = KafkaConsumer(
        'dbserver1.inventory.customers',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    # Construct a BigQuery client object.


    fichier = open("data/customer.csv", "a")

    # TODO(developer): Set table_id to the ID of table to append to.
    # table_id = "your-project.your_dataset.your_table"

    paris_tz = pytz.timezone('Europe/Paris')
    i=1
    for message in consumer:
        if message.value != None:
            consumer_data = json.loads(message.value)
            op = consumer_data['payload']['op']
            ts_ms_int = int(consumer_data['payload']['ts_ms'])
            ts_ms = float(consumer_data['payload']['ts_ms'])/1000
            # convert to datetime
            ts_str=datetime.fromtimestamp(ts_ms).strftime('%Y-%m-%d %H:%M:%S:%f')
            ts_str_utc=datetime.utcfromtimestamp(ts_ms).strftime('%Y-%m-%d %H:%M:%S:%f')
            ts_str_tz=datetime.utcfromtimestamp(ts_ms).astimezone(paris_tz).strftime('%Y-%m-%d %H:%M:%S:%f')
            if op == 'd':
                id = consumer_data['payload']['before']['id']
                first_name = consumer_data['payload']['before']['first_name']
                last_name = consumer_data['payload']['before']['last_name']
                email = consumer_data['payload']['before']['email']
            else:
                id = consumer_data['payload']['after']['id']
                first_name = consumer_data['payload']['after']['first_name']
                last_name = consumer_data['payload']['after']['last_name']
                email = consumer_data['payload']['after']['email']
    
            #print(ts_ms,  "TS > ",ts_str, "TS UTC > ", ts_str_utc, "TS Local Time >", ts_str_tz)
            #print(op, id, first_name, last_name, email)
            #print("====== payload =====")
            #print(consumer_data['payload'])
            #print("====== schema =====")
            #print(consumer_data['schema'])
            #print("===================")
            #print(consumer_data)
            print("======"*15)
            print(i, ts_ms,  "TS > ",ts_str, "TS UTC > ", ts_str_utc, "TS Local Time >", ts_str_tz)
            print(i,op, id, first_name, last_name, email)
            if op == 'u':
                print("=====DEEPDIFF======")
                bef=consumer_data['payload']['before']
                aft=consumer_data['payload']['after']
                print(DeepDiff(bef, aft))
    
            rows_to_insert = "{}|{}|{}|{}|{}|{}|{}\n".format(op, ts_ms_int, ts_str_tz, id, first_name, last_name, email)
            
            errors = fichier.write(rows_to_insert)  # Make an API request.
            if errors != 0:
                print("New rows have been added. id = {}".format(id))
                fichier.flush()
            else:
                print("Encountered errors while inserting rows: {}".format(errors))
            i=i+1
