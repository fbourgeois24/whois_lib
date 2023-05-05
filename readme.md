# Récupération des information sur le site Whois de la Lifras

## Importer la blbliothèque
`from whois_lib.whois_lib import whois`

## Utiliser la fonction whois
Il y a deux possibilités de recherche sur le site whois:
1) nom + ID lifras
2) nom + prénom + date de naissance

`whois_data = whois(nom='nom', prenom='prenom', dna='dna', id_lifras='lifras_id')`
Il y a donc lieu de spécifier la bonne combinaison de paramètres à l'appel de la fonction.
S'il manque des paramètres, la fonction renvoie le dictionnaire suivant
`{"statut": False, "result":"Il faut entrer le prénom et la date de naissance OU l'id lifras"}`

### Dictionnaire renvoyé par la fonction
La fonction renvoie toujours un dictionnaire, les clés suivantes peuvent être présentes:
| Clé | Type de donnée | Explication |
| statut | booléen | Cette clé est toujours présente, sa valeur est à vrai (True) si la requête a réussi et a trouvé la personne. Si pas elle sera à faux (False) |
| result | string | Cette clé n'est présente que si statut = False, autrement dit s'il y a eu un problème. Elle contient la description du problème rencontré. Hormis statut, seule cette clé est présente en cas d'erreur (statut = False) |
| prenom | string | Prénom |
| nom | string | Nom |
| dna | datetime.date | Date de naissance |
| id lifras | string | ID Lifras|
| statut medic | booléen | True si statut médical en ordre et False si non |
| date medic | datetime.date | Date jusqu'à laquelle le certificat médical est valable (None si certificat médical plus valable, dans ce cas 'statut medic' sera à False) |
| ice | string | Numéro ICE |
| aig | string | Numéro d'appel AIG |
| police | string | Numéro de police d'assurance |
| brevets | dictionnaire {string: datetime.date} | Dictionnaire contenant la liste des brevets, la clé est le nom du brevet et la valeur est la date d'obtention |
| en ordre | booléen | True si le membre est en ordre administrativement et False si non. Depuis la suppression de l'ECG, cette clé renvoi la même valeur que 'statut medic' |


Si une erreur survient, la fonction renverra donc par exemple : {'statut': False, 'result': 'Membre inconnu'}
Si les infos ont correctement été récupérées, la fonction renverra par exemple (donnée altérées pour l'exemple) : {'statut': True, 'prenom': 'François', 'nom': 'BOURGEOIS', 'dna': datetime.date(1998, 4, 12), 'id lifras': 12345, 'statut medic': True, 'date medic': datetime.date(2099, 1, 31), 'ice': '321234567890', 'aig': '+323 222.11.33', 'police': '3.123.456/789', 'brevets': {'Nom du brevet': datetime.date(2022, 2, 25), 'Autre brevet': datetime.date(1990, 6, 1)}, 'en ordre': True}