#!/usr/bin/python
#coding: utf-8

import os, urllib, re, time, subprocess
from xml.dom import minidom


emissions=[
[48,"Guignols","http://www.canalplus.fr/c-divertissement/pid1784-c-les-guignols.html?vid=%s"],
[201,"Zapping","http://www.canalplus.fr/c-infos-documentaires/pid1830-c-zapping.html?vid=%s"]
]

homedir = os.path.expanduser('~')
output_dir = homedir + "/Téléchargements/"
historique = output_dir + ".cplus_hist"

class Canal :

	__urlXMLMEA = 'http://service.canal-plus.com/video/rest/getMEAs/cplus/%s'

	def __init__(self,CodeEmission="", NomEmission="", UrlEmission=""):
		self.CodeEmission = CodeEmission
		self.NomEmission = NomEmission
		self.UrlEmission = UrlEmission

	def __GetDate(self,i):
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

	def __ParseXmlMea(self,xmldoc):
		ids = []
		meas = xmldoc.getElementsByTagName('MEA')
		for i in meas:
			if i.getElementsByTagName('ID')[0].childNodes != []:
				id = i.getElementsByTagName('ID')[0].childNodes[0].nodeValue
				titre = i.getElementsByTagName('TITRE')[0].childNodes[0].nodeValue
				if 'semaine' not in titre.lower():
					ids.append([id,self.NomEmission,titre,self.__GetDate(i)])
		return ids

	def __downloadXml(self,url):
		try:
			xmlFile = urllib.urlopen(url).read()
		except Exception :
			return 1
		try:
			xmldoc = minidom.parseString(xmlFile)
		except Exception :
			xmldoc = 1
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
		cmd_args = ['youtube-dl','-f','best', "-o", output_dir+"%(title)s.%(ext)s", url % str(episode_emission)]
		p = subprocess.Popen(cmd_args)
		return p.wait()

	def __GetUrlXmlMea(self,code):
		return self.__urlXMLMEA % code

	def download(self):
		UrlXmlMea = self.__GetUrlXmlMea(self.CodeEmission)
		XmlMea = self.__downloadXml(UrlXmlMea)
		ListID = self.__ParseXmlMea(XmlMea)
		for episode_emission in ListID :
			log_emission = episode_emission[1]+"|"+episode_emission[3]
			if not self.__checkHistory(log_emission) :
				if self.__youtubeDl(self.UrlEmission,episode_emission[0]) == 0 :
					self.__addHistory(log_emission)



for emission in emissions:
	MyVideo = Canal(CodeEmission=emission[0],NomEmission=emission[1],UrlEmission=emission[2])
	MyVideo.download()
