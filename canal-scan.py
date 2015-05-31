# coding: utf-8

import os, re, time, subprocess, xml.dom.minidom, operator

try:
	import urllib.request as compat_urllib_request
except:  # Python 2
	import urllib2 as compat_urllib_request

homedir = os.path.expanduser('~')

# Dossier ou les vidéos sont sauvegardées
scan_emission = homedir + "/dev/canal-quotidienne/cplus_scan.txt"

playlistdir = homedir + "/dev/canal-quotidienne/playlists/"

class CanalScan :

	# URL de toutes les vidéos d'une émission donnée.
	__urlXmlMea = 'http://service.canal-plus.com/video/rest/getMEAs/cplus/{}'

	def __init__(self):
		self.__checkScanFile()

	def __checkScanFile(self):
		if not os.path.isfile(scan_emission) :
			file = open(scan_emission, 'w')
			file.close()
		else :
			os.remove(scan_emission)

	def __parseXml(self,xmldoc):
		rubriques = []
		meas = xmldoc.getElementsByTagName('MEA')
		for i in meas:
			if i.getElementsByTagName('ID')[0].childNodes != []:
				emission = i.getElementsByTagName('RUBRIQUE')[0].childNodes[0].nodeValue
				rubriques.append(str(emission))
		return rubriques

	def __comptage(self,rubriques):
		dictionnaire = {}
		for rubrique in rubriques :
			dictionnaire[rubrique] = dictionnaire.get(rubrique,0) + 1
		return self.__triNumeriquePuisAlphabetiqueSousListe(list(dictionnaire.items()))

	def __triNumeriquePuisAlphabetiqueSousListe(self,liste) :
		return sorted(liste, key  = lambda x: (-x[1], x[0]))

	def __downloadXml(self,url):
		try:
			xmlFile = compat_urllib_request.urlopen(url).read()
		except:
			print("Problème de téléchargement, réessayez plus tard")
			exit()
		return xmlFile

	def __parseXmlMea(self,xmlFile) :
		return xml.dom.minidom.parseString(xmlFile)

	def __savePlaylist(self,xmlFile,codePlaylist):
		playlistFile = playlistdir+str(codePlaylist)+".xml"
		file = open(playlistFile, 'wb')
		file.write(xmlFile)
		file.close()

	def __logComptage(self,codePlaylist,Comptage):
		file = open(scan_emission, 'a')
		file.write(str(codePlaylist) + '\n')
		file.write(str(Comptage) + '\n\n')
		file.close()

	def __geturlXmlMea(self,code):
		return CanalScan.__urlXmlMea.format(code)

	def __openPlaylist(self,pathPlaylist):
		if os.path.isfile(pathPlaylist) :
			file = open(pathPlaylist, 'r')
			contenuXml = file.read()
			file.close()
			return contenuXml
		else :
			return False

	def downloadPlaylists(self):
		for codePlaylist in list(range(0,3900)) :
			print("playlist "+str(codePlaylist))
			urlXmlMea = self.__geturlXmlMea(codePlaylist)
			xmlMea = self.__downloadXml(urlXmlMea)
			rubriquesXml = self.__parseXmlMea(xmlMea)
			rubriques = self.__parseXml(rubriquesXml)
			if len(rubriques)>0 :
				self.__savePlaylist(xmlMea,codePlaylist)

	def scanPlaylists(self):
		for codePlaylist in list(range(0,3900)) :
			pathPlaylist = playlistdir+str(codePlaylist)+".xml"
			xmlMea = self.__openPlaylist(pathPlaylist)
			if xmlMea != False :
				rubriquesXml = self.__parseXmlMea(xmlMea)
				rubriques = self.__parseXml(rubriquesXml)
				if len(rubriques)>0 :
					comptage = self.__comptage(rubriques)
					self.__logComptage(codePlaylist,comptage)


if __name__ == "__main__":

	myVideo = CanalScan()
	myVideo.downloadPlaylists()
	myVideo.scanPlaylists()