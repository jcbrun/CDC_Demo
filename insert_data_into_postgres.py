import psycopg2

try:
    connection = psycopg2.connect(user="docker",
                                  password="docker",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="bitcoindb")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO coins (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
    record_to_insert = (2, 'Kafka and Debezium', 5636)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into coins table", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")