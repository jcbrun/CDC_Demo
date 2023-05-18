import json
from kafka import KafkaConsumer
from datetime import datetime
import pytz
from google.cloud import bigquery
from google.oauth2 import service_account
from time import sleep
from deepdiff import DeepDiff

print("Waiting on Messages ...")
if __name__ == '__main__':
    consumer = KafkaConsumer(
        'dbserver1.inventory.customers',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

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
            #parsed = json.loads(consumer_data)
            # Affiche le JSON indenté
            #print(json.dumps(consumer_data['payload'], indent=4))
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
            #print(i, op, id, first_name, last_name, email)
            #print("====== payload =====")
            #print(consumer_data['payload'])
            #print("====== schema =====")
            #print(consumer_data['schema'])
            #print("===================")
            #print(consumer_data)
            #print(ts_ms,  "TS > ",ts_str, "TS UTC > ", ts_str_utc, "TS Local Time >", ts_str_tz)
            print(i,' : ', op,' : ', id,' : ', first_name,' : ', last_name,' : ', email)
            #print("===================")
            if op == 'u':
                print("=====DEEPDIFF======")
                print(DeepDiff(consumer_data['payload']['before'], consumer_data['payload']['after']))
            print("======"*15)
            i=i+1
    
