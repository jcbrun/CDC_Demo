echo "Usage : $0 val_deb nb_valeur"

val_deb=$1
nb_valeur=$2
i=0

while [[ $i -ne $nb_valeur ]]
do
	val_tmp=$(($val_deb + $i))
	echo $val_tmp
	curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   		"email": "jcbrun_'$val_tmp'@gmail.com",
   		"fname": "prenom_'$val_tmp'",
   		"id": "'$val_tmp'",
   		"lname": "nom_'$val_tmp'"
 	}' 'http://127.0.0.1:5001/api/people'
	i=$((i + 1))
done
