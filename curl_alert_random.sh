echo "Usage : $0 val_deb nb_valeur"

val_deb=$1
nb_valeur=$2
i=1


elapse=$(($RANDOM%10))
echo "elapse : $elapse"

while true
do
	val_rand=$(($RANDOM%$nb_valeur))
	val_tmp=$(($val_deb + $val_rand))
	echo $val_tmp

	curl -X PUT --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ 
   		"email": "mail_'$val_tmp'@danger.com",
   		"fname": "prenom_'$val_tmp'",
   		"id": "'$val_tmp'",
   		"lname": "nom_'$val_tmp'"
	}' 'http://127.0.0.1:5001/api/people/'$val_tmp
	sleep $elapse
        elapse=$(($RANDOM%10))
	echo "Nb mise à jour : $i"
	i=$((i + 1))
done
