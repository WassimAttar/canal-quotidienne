#!/usr/bin/python
#coding: utf-8

import os, re, time, subprocess
from xml.dom import minidom

try:
    import urllib.request as compat_urllib_request
except ImportError:  # Python 2
    import urllib2 as compat_urllib_request


emissions=[
[48,"Guignols"],
[201,"Zapping"],

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
outputdir = homedir + "/Téléchargements/"
historique = outputdir + ".cplus_hist"

class Canal :

	__urlXmlMea = 'http://service.canal-plus.com/video/rest/getMEAs/cplus/%s'

	# L'URL pour télécharger une vidéo peut être quelconque.
	# Ce qui importe est le numéro envoyé à la variable vid.
	# Nous pouvons donc envoyer un numéro vid du Zapping avec une URL des Guignols.
	# Par défaut, l'URL choisie est celle des Guignols mais on peut utiliser l'URL du Zapping
	# http://www.canalplus.fr/c-infos-documentaires/pid1830-c-zapping.html

	__urlVideo = 'http://www.canalplus.fr/c-divertissement/pid1784-c-les-guignols.html?vid=%s'

	__codeEmission = ""
	__nomEmission = ""

	def __init__(self,emission):
		self.__codeEmission = emission[0]
		self.__nomEmission = emission[1]

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
		xmlFile = compat_urllib_request.urlopen(url).read()
		xmldoc = minidom.parseString(xmlFile)
		return xmldoc

	def __checkHistory(self,log_emission):
		file = open(historique, 'r')
		for line in file:
			if log_emission+'\n' == line:
				return True
		return False

	def __addHistory(self,log_emission):
		file = open(historique, 'a')
		file.write(log_emission.encode('utf-8') + '\n')
		file.close()

	def __youtubeDl(self,url,episode_emission):
		cmd_args = ['youtube-dl','-f','best', "-o", outputdir+"%(title)s.%(ext)s", url % str(episode_emission)]
		p = subprocess.Popen(cmd_args)
		return p.wait()

	def __geturlXmlMea(self,code):
		return self.__urlXmlMea % code

	def download(self):
		urlXmlMea = self.__geturlXmlMea(self.__codeEmission)
		xmlMea = self.__downloadXml(urlXmlMea)
		listID = self.__parseXmlMea(xmlMea)
		for episode_emission in listID :
			log_emission = episode_emission[1]+"|"+episode_emission[3]
			if not self.__checkHistory(log_emission) :
				if self.__youtubeDl(self.__urlVideo,episode_emission[0]) == 0 :
					self.__addHistory(log_emission)



for emission in emissions:
	myVideo = Canal(emission)
	myVideo.download()
