""" Récupérer les informations du site whois de la Lifras """

import requests
from datetime import datetime as dt


def whois(nom, prenom, dna):
	""" Récupérer les infos sur base du nom, prénom et date de naissance
		
	"""

	# Entête de la requête
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	# Corps de la requête
	data = {'Nom':nom.encode('ISO-8859-1'),'Prenom':prenom.encode('ISO-8859-1'), 'Naissance':dna, 'Action':'Search','ClubID':'202','LG':'FR'}
	
	result = requests.post('https://www9.iclub.be/whois2.asp', headers=headers, data=data)

	if "No member founded" in result.text:
		return {"status": False, "result":"No member founded"}

	form = result.text[result.text.index("<form"):result.text.index("</form>")]
	form_lines = form.split("\n")
	prenom = form_lines[2].split('value="')[1].split('"')[0]
	nom = form_lines[4].split('value="')[1].split('"')[0]
	dna_AAAAMMJJ = form_lines[7].split('value="')[1].split('"')[0]
	dna = f"{dna[:2]}/{dna[3:5]}/{dna[-4:]}"
	id_lifras = form_lines[11].split('value="')[1].split('"')[0]
	ice = result.text.split("ICE <b>")[1].split("</b>")[0]
	aig = result.text.split(" AIG Call center ")[1].split("</b>")[0]
	text = result.text.split("fa-medkit")[1].split("</i>")[1].split("</div>")[0]
	if "Medical situation in order !" in text:
		medic_status = True
		medic_date = dt.strptime(text.split('Valid to ')[1], '%d/%m/%Y')
	else:
		medic_status = False
		medic_date = None
	
	text = result.text.split("fa-heartbeat")[1].split("</i>")[1].split("</div>")[0]
	if " ECG in order !" in text:
		ecg_status = True
		ecg_date = dt.strptime(text.split('Valid to ')[1], '%d/%m/%Y')
	else:
		ecg_status = False
		ecg_date = None

	certifications_table = result.text.split('<table class="table table-striped table-condensed">')[1].split("</table>")[0]
	brevets = {}
	for certification in certifications_table.split("<tr>")[1:]:
		brevet = certification.replace('<td><i class="fa fa-certificate"></i> ', "").split("</td><td>")[0]
		if "No certification founded !" in brevet:
			break
		date = certification.split("</td><td>")[1].split("</td></tr>")[0]
		brevets[brevet] = date

	return {"status": True, "prenom": prenom, "nom":nom, "dna": dna, "id lifras": id_lifras, "statut ECG": ecg_status, "date ECG": ecg_date, 
	"statut medic": medic_status, "date medic": medic_date, "ice": ice, "aig": aig, "brevets": brevets}


if __name__ == "__main__":
	print(whois("Bourgeois", "François", "24/06/1994"))