# coding: utf-8

import os, xml.dom.minidom, sys, mysql.connector

homedir = os.path.expanduser('~')

playlistdir = homedir + "/dev/canal-quotidienne/playlists/"

class CanalImportXml :

	# URL de toutes les vidéos d'une émission donnée.
	__balisesXml = ("ID","TITRE","SOUS_TITRE","UNIVERS","RUBRIQUE","CATEGORIE")

	def __init__(self):
		if sys.version_info < (3,) :
			print("Script à lancer avec python3")
			exit()
		self.__requete_header = "INSERT INTO emissions (IDPL,"
		for balise in CanalImportXml.__balisesXml :
			self.__requete_header += str(balise)+","
		self.__requete_header = self.__requete_header[:-1] + ") VALUES ("
		tmp = "%s,"*(len(CanalImportXml.__balisesXml)+1)
		tmp = tmp[:-1]
		self.__requete_header += tmp + ")"

		self.__instanceMysql = mysql.connector.connect(host="localhost",user="root",password="", database="canal")
		self.__cursor = self.__instanceMysql.cursor()

		self.__cursor.execute("TRUNCATE emissions")
		self.__instanceMysql.commit()


	def __del__(self):
		self.__instanceMysql.close()

	def __parseXml(self,xmldoc):
		emissions = []
		meas = xmldoc.getElementsByTagName('MEA')
		for i in meas:
			tmp = []
			for balise in CanalImportXml.__balisesXml :
				try :
					tmp.append(str(i.getElementsByTagName(balise)[0].childNodes[0].nodeValue))
				except IndexError :
					tmp.append("")
			emissions.append(tmp)
		return emissions

	def __parseXmlMea(self,xmlFile) :
		return xml.dom.minidom.parseString(xmlFile)

	def __openPlaylist(self,pathPlaylist):
		if os.path.isfile(pathPlaylist) :
			file = open(pathPlaylist, 'r')
			contenuXml = file.read()
			file.close()
			return contenuXml
		else :
			return False

	def __sql(self,codePlaylist,emissions) :
		for emission in emissions :
			emission.insert(0,codePlaylist)
			self.__cursor.execute(self.__requete_header, emission)
		self.__instanceMysql.commit()

	def importPlaylists(self):
		for codePlaylist in list(range(0,4000)) :
			pathPlaylist = playlistdir+str(codePlaylist)+".xml"
			xmlMea = self.__openPlaylist(pathPlaylist)
			if xmlMea != False :
				emissionsXml = self.__parseXmlMea(xmlMea)
				emissions = self.__parseXml(emissionsXml)
				if len(emissions)>0 :
					print("import playlist "+str(codePlaylist))
					requetes = self.__sql(codePlaylist,emissions)


if __name__ == "__main__":

	myVideo = CanalImportXml()
	myVideo.importPlaylists()