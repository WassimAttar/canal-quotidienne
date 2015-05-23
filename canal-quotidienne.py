#!/usr/bin/python
#coding: utf-8

import os, re, time, subprocess, xml.dom.minidom

try:
	import urllib.request as compat_urllib_request
except:  # Python 2
	import urllib2 as compat_urllib_request


emissions=[
[48,"Guignols"],
[201,"Zapping"],

# [121,"Bandes de filles"],
# [14,"Le Cercle"],
# [39,"Connasse"],
# [130,	"Action discrete"],
# [304,	"Action discrete"],
# [371,	"Action discrete"],
# [62,	"Le boucan du jour"],
# [627,	"Bref"],
# [104,	"Le grand journal"],
# [254,	"Groland"],
# [242,	"Du hard ou du cochon"],
# [451,	"Jamel comedy club"],
# [896,	"Le journal du hard"],
# [39,	"La matinale"],
# [215,	"Le meilleur du hier"],
# [47,	"Les pépites du net"],
# [249,	"Petit journal [le)"],
# [843,	"La question de plus"])
# [294,	"La revue de presse de Catherine et Eliane"],
# [1082,"Salut les terriens"],
# [41,	"Salut les terriens"],
# [74,	"Salut les terriens"],
# [105,	"Salut les terriens"],
# [110,	"Salut les terriens"],
# [316,	"Salut les terriens"],
# [371,	"Salut les terriens"],
# [680,	"Salut les terriens - edito de Blako"],
# [1064,"Salut les terriens - Gaspard Proust"],
# [1072,"Salut les terriens - les martiens de la semaine"],
# [252,	"SAV des émissions"],
# [936,	"Tweet en clair"],

]

homedir = os.path.expanduser('~')

# Dossier ou les vidéos sont sauvegardées
outputdir = homedir + "/Téléchargements/"

# Fichier de l'historique des vidéos déjà téléchargées
historique = outputdir + ".cplus_historique"

class Canal :

	# URL de toutes les vidéos d'une émission donnée.
	__urlXmlMea = 'http://service.canal-plus.com/video/rest/getMEAs/cplus/{}'

	# L'URL pour télécharger une vidéo peut être quelconque.
	# Ce qui importe est le numéro envoyé à la variable vid.
	# Nous pouvons donc envoyer un numéro vid du Zapping avec une URL des Guignols.
	# Par défaut, l'URL choisie est celle des Guignols mais on peut utiliser l'URL du Zapping.
	# http://www.canalplus.fr/c-infos-documentaires/pid1830-c-zapping.html
	__urlVideo = 'http://www.canalplus.fr/c-divertissement/pid1784-c-les-guignols.html?vid={}'

	__codeEmission = ""
	__nomEmission = ""

	def __init__(self):
		self.__checkYoutubeDlInstallation()
		self.__checkHistoryFile()

	def __checkYoutubeDlInstallation(self):
		try:
			subprocess.call(["youtube-dl","--version"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except:
			print("youtube-dl non installé. Pour installer la dernière version, taper cette commande :\nsudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/bin/youtube-dl && sudo chmod 755 /usr/bin/youtube-dl")
			exit()

	def __checkHistoryFile(self):
		if not os.path.isfile(historique) :
			file = open(historique, 'w+')
			file.close()

	# Les dates fournies par canal ne sont pas toujours bien formatées.
	# Parfois c'est 02/05/2015 ou 02/05/15 ou 02/05
	# Pour avoir l'historique et donc éviter de télécharger plusieurs fois la même émission
	# il est nécessaire de formater toujours de la même façon la date de diffusion de l'émission.
	# La forme choisie est la suivante 02/05/15
	def __getDate(self,i):
		L = ['TITRE','SOUS_TITRE']
		grep_date_annee_complete = '[0-9]{2}/[0-9]{2}/[0-9]{4}'
		grep_date_annee = '[0-9]{2}/[0-9]{2}/[0-9]{2}'
		grep_date_mois = '[0-9]{2}/[0-9]{2}'
		for balise in L:
			valeur = i.getElementsByTagName(balise)[0].childNodes[0].nodeValue
			if re.search(grep_date_annee_complete, valeur):
				temp = re.findall(grep_date_annee_complete, valeur)[0]
				return temp[0:6]+temp[8:10]
			elif re.search(grep_date_annee, valeur):
				return re.findall(grep_date_annee, valeur)[0]
			elif re.search(grep_date_mois, valeur):
				return re.findall(grep_date_mois, valeur)[0]+"/"+time.strftime("%y")
		return ""

	def __parseXmlMea(self,xmldoc):
		ids = []
		meas = xmldoc.getElementsByTagName('MEA')
		for i in meas:
			if i.getElementsByTagName('ID')[0].childNodes != []:
				id = i.getElementsByTagName('ID')[0].childNodes[0].nodeValue
				titre = i.getElementsByTagName('TITRE')[0].childNodes[0].nodeValue
				if 'semaine' not in titre.lower():
					ids.append([id,self.__nomEmission,titre,self.__getDate(i)])
		return ids

	def __downloadXml(self,url):
		try:
			xmlFile = compat_urllib_request.urlopen(url).read()
		except:
			print("Problème de téléchargement, réessayez plus tard")
			exit()
		xmldoc = xml.dom.minidom.parseString(xmlFile)
		return xmldoc

	def __checkHistory(self,log_emission):
		file = open(historique, 'r')
		for line in file:
			if log_emission+'\n' == line:
				file.close()
				return True
		file.close()
		return False

	# L'historique des téléchargements est sous la forme
	# Guignols|18/05/15
	# Zapping|18/05/15
	def __addHistory(self,log_emission):
		file = open(historique, 'a')
		file.write(log_emission + '\n')
		file.close()

	# youtube-dl se charge de télécharger la vidéo.
	# La qualité est toujours à best
	def __youtubeDl(self,url,episode_emission):
		cmd_args = ['youtube-dl','-f','best', "-o", outputdir+"%(title)s.%(ext)s", url.format(episode_emission)]
		p = subprocess.Popen(cmd_args)
		return p.wait()

	def __geturlXmlMea(self,code):
		return self.__urlXmlMea.format(code)

	def download(self,emission):
		self.__codeEmission = emission[0]
		self.__nomEmission = emission[1]
		urlXmlMea = self.__geturlXmlMea(self.__codeEmission)
		xmlMea = self.__downloadXml(urlXmlMea)
		listID = self.__parseXmlMea(xmlMea)
		for episode_emission in listID :
			log_emission = episode_emission[1]+"|"+episode_emission[3]
			if not self.__checkHistory(log_emission) :
				if self.__youtubeDl(self.__urlVideo,episode_emission[0]) == 0 :
					self.__addHistory(log_emission)



for emission in emissions:
	myVideo = Canal()
	myVideo.download(emission)