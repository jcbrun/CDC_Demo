import psycopg2
try:
    conn = psycopg2.connect(
          user = "postgres",
          password = "postgres",
          host = "localhost",
          port = "5432",
          database = "postgres"
    )
    cur = conn.cursor()
    # Afficher la version de PostgreSQL 
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version : ", version,"\n")

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventory.customers (ID, FIRST_NAME, LAST_NAME, EMAIL) VALUES
        (1,'Paul', 'Fouchet','paul@fouchet.com'),
        (2,'Adrien', 'dubois','adriendb@gmail.com')
    """)
    conn.commit()

    cur.execute("SELECT * FROM inventory.customers")
    rows = cur.fetchall()
    for data in rows:
        print("ID :" + str(data[0]))
        print("PRENOM :" + data[1])
        print("NAME :" + data[2])
        print("EMAIL :" + data[3])
        print("== "*5)

    print('Data récupérée avec succès')
  
    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)
