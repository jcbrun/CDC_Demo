# Instruction pour demo

ouvrir 3 fenetres iTerm

1/ Principale
-   se connecter à VM GCP : gcloud compute ssh --project=ambient-antenna-369806 --zone=europe-west9-a ud-instance-2
-	lancer : cd ~/projets/41_postgres_debezium_kafka_python/;source venv41/bin/activate;  export DEBEZIUM_VERSION=1.9
-	Netoyer BigQuery : python3 clean_bigquery.py
-	./launch.sh  (Permet de lancer les différent composant docker)

2/ Fenetre people App
-	lancer : cd ~/projets/41_postgres_debezium_kafka_python/;source venv41/bin/activate;  export DEBEZIUM_VERSION=1.9
- 	python3 apiPeoplePostgres/server.py

3/ Fenetre Tunnel
-	gcloud compute ssh --project=ambient-antenna-369806 --zone=europe-west9-a ud-instance-2 -- -NL 5001:localhost:5001

4/ Démarrer une fenetre chrome
-	se connecter à : http://127.0.0.1:5001/
-	montrer les 4 records

5/ Lancer une fenetre big query
-	montrer que la table est vide∏

6/ Principale 
-	lancer le consumer : python3 consumer_to_bigquery.py 
-	Montrer que les 4 record sont répliqué en init dans la queu
-	et montrer que nous les avons aussi envoyé à big query

7/ dans l'app People
-	creer une personne
	-	montrer qu'elle est presente dans le consommateur
	-	montrer que présente dans big query
-	mettre à jour une personne
	-	montrer qu'elle est presente dans le consommateur
	-	montrer que présente dans big query
-	supprimer une personne
	-	montrer qu'elle est presente dans le consommateur
	-	montrer que présente dans big query

8/ Manipulation postgres

docker exec -it cdc_demo-postgres-1 psql -U postgres
\c postgres
select * from inventory.customers;
