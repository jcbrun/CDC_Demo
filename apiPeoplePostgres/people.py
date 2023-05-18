"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime
import psycopg2

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


conn = psycopg2.connect(
      user = "postgres",
      password = "postgres",
      host = "localhost",
      port = "5432",
      database = "postgres"
)

PEOPLE={}

cur = conn.cursor()
cur.execute("SELECT * FROM inventory.customers")
rows = cur.fetchall()
result_dict = []
for data in rows:
    PEOPLE.update({
        str(data[0]): {
           'id': str(data[0]), 
           'fname': str(data[1]), 
           'lname': str(data[2]), 
           'email': str(data[3]) 
        }
    })
cur.close()
conn.close()


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        json string of list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    #return result_dict 


def read_one(id):
    """
    This function responds to a request for /api/people/{id}
    with one matching person from people

    :param id:   ID of person to find
    :return:        person matching ID
    """
    # Does the person exist in people?
    if id in PEOPLE:
        person = PEOPLE.get(id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with ID {id} not found".format(id=id)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data

    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    id = person.get("id", None)
    fname = person.get("fname", None)
    lname = person.get("lname", None)
    email = person.get("email", None)

    # Does the person exist already?
    if id not in PEOPLE and id is not None:
        PEOPLE[id] = {
            "id": id,
            "fname": fname,
            "lname": lname,
            "email": email,
            "timestamp": get_timestamp(),
        }
        conn = psycopg2.connect(
          user = "postgres",
          password = "postgres",
          host = "localhost",
          port = "5432",
          database = "postgres"
          )
        cur = conn.cursor()
        sql = """INSERT INTO inventory.customers (ID, FIRST_NAME, LAST_NAME, EMAIL) VALUES
            (%s,%s,%s,%s)"""
        value = (id, fname, lname, email)
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()
        return PEOPLE[id], 201

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Peron with ID {id} already exists".format(id=id),
        )


def update(id, person):
    """
    This function updates an existing person in the people structure

    :param id:   ID of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if id in PEOPLE:
        PEOPLE[id]["fname"] = person.get("fname")
        fname = person.get("fname")
        PEOPLE[id]["lname"] = person.get("lname")
        lname = person.get("lname")
        PEOPLE[id]["email"] = person.get("email")
        email = person.get("email")
        PEOPLE[id]["timestamp"] = get_timestamp()

        conn = psycopg2.connect(
          user = "postgres",
          password = "postgres",
          host = "localhost",
          port = "5432",
          database = "postgres"
          )
        cur = conn.cursor()
        sql = """UPDATE inventory.customers SET FIRST_NAME=%s, LAST_NAME=%s, EMAIL=%s
                     WHERE ID=%s"""
        value = (fname, lname, email, id)
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        conn.close()

        return PEOPLE[id]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with ID {id} not found".format(id=id)
        )


def delete(id):
    """
    This function deletes a person from the people structure

    :param id:   ID of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if id in PEOPLE:
        del PEOPLE[id]

        conn = psycopg2.connect(
          user = "postgres",
          password = "postgres",
          host = "localhost",
          port = "5432",
          database = "postgres"
          )
        cur = conn.cursor()
        #sql = """DELETE FROM inventory.customers WHERE ID=%s""".format(id)
        sql = """DELETE FROM inventory.customers WHERE ID={}""".format(id)
        ##value = id
        ##cur.execute(sql, value)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return make_response( "{id} successfully deleted".format(id=id), 200)

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with ID {id} not found".format(id=id)
        )
