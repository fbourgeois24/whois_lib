""" Récupérer les informations du site whois de la Lifras """

import requests
from datetime import datetime as dt
import logging as log

# log.basicConfig(level=10)


def whois(nom, prenom="", dna="", id_lifras=""):
	""" Récupérer les infos sur base du nom, prénom et date de naissance
		
	"""

	if (prenom.replace(" ","") == "" or dna.replace(" ","") == "") and id_lifras.replace(" ","") == "":
		raise ValueError("Il faut entrer le prénom et ou la date de naissance OU l'id lifras")

	# Entête de la requête
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	# Corps de la requête
	data = {'Nom':nom.encode('ISO-8859-1'),'Prenom':prenom.encode('ISO-8859-1'), 'Naissance':dna, "Nom1":nom.encode('ISO-8859-1'), 
		"NrFederation2": id_lifras, 'Action':'Search','ClubID':'202','LG':'FR'}
	
	result = requests.post('https://www9.iclub.be/whois2.asp', headers=headers, data=data)
	# log.debug(result.text)

	if "No member founded" in result.text:
		return {"status": False, "result":"Membre inconnu"}

	form = result.text[result.text.index("<form"):result.text.index("</form>")]
	form_lines = form.split("\n")
	# for seq, line in enumerate(form_lines):
	# 	log.debug(f"{seq}: {line}")
	prenom = form_lines[2].split('value="')[1].split('"')[0]
	nom = form_lines[4].split('value="')[1].split('"')[0]
	dna = dt.strptime(form_lines[7].split('value="')[1].split('"')[0], "%d/%m/%Y").date()
	id_lifras = int(form_lines[11].split('value="')[1].split('"')[0])
	ice = result.text.split("ICE <b>")[1].split("</b>")[0]
	aig = result.text.split(" AIG Call center ")[1].split("<br>")[0]
	police = result.text.split(" AIG Call center ")[1].split("<br>Police ")[1].split("</b>")[0]
	text = result.text.split("fa-medkit")[1].split("</i>")[1].split("</div>")[0]
	if "Medical situation in order !" in text:
		medic_status = True
		medic_date = dt.strptime(text.split('Valid to ')[1], '%d/%m/%Y').date()
	else:
		medic_status = False
		medic_date = None
	
	text = result.text.split("fa-heartbeat")[1].split("</i>")[1].split("</div>")[0]
	if " ECG in order !" in text:
		ecg_status = True
		ecg_date = dt.strptime(text.split('Valid to ')[1], '%d/%m/%Y').date()
	else:
		ecg_status = False
		ecg_date = None

	certifications_table = result.text.split('<table class="table table-striped table-condensed">')[1].split("</table>")[0]
	brevets = {}
	for certification in certifications_table.split("<tr>")[1:]:
		brevet = certification.replace('<td><i class="fa fa-certificate"></i> ', "").split("</td><td>")[0]
		if "No certification founded !" in brevet:
			break
		date = dt.strptime(certification.split("</td><td>")[1].split("</td></tr>")[0], "%d/%m/%Y").date()
		brevets[brevet] = date


	return {"statut": True, "prenom": prenom, "nom":nom, "dna": dna, "id lifras": id_lifras, "statut ecg": ecg_status, "date ecg": ecg_date, 
	"statut medic": medic_status, "date medic": medic_date, "ice": ice, "aig": aig, "police":police, "brevets": brevets, "en ordre": ecg_status and medic_status}


if __name__ == "__main__":
	print(whois("Bourgeois", id_lifras="74065", ))
	# print(whois("Bourgeois", "François", "24/06/1994"))