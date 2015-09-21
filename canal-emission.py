# coding: utf-8

import os, sys, mysql.connector, collections

equivalent = {"GUIGNOLS" : "LES_GUIGNOLS"}

class CanalPlaylist :

	def __init__(self):
		if sys.version_info < (3,) :
			print("Script à lancer avec python3")
			exit()

		self.__instanceMysql = mysql.connector.connect(host="localhost",user="root",password="", database="canal")
		self.__cursor = self.__instanceMysql.cursor()

	def __del__(self):
		self.__instanceMysql.close()

	def __calculPlaylists(self):
		listePlaylist = []
		sql_0 = "SELECT distinct(IDPL) FROM emissions where IDPL<4000"
		self.__cursor.execute(sql_0)
		results_0 = self.__cursor.fetchall()
		for row_0 in results_0:
			IDPL = row_0[0]
			sql_1 = "select rubrique from emissions where IDPL='%s'"
			self.__cursor.execute(sql_1,(IDPL,))
			results_1 = self.__cursor.fetchall()
			dictionnaire = {}
			for row_1 in results_1:
				RUBRIQUE = row_1[0]
				dictionnaire[RUBRIQUE] = dictionnaire.get(RUBRIQUE,0) + 1
			listePlaylist.append((IDPL,dictionnaire))
		return listePlaylist

	def __extractUnique(self,listePlaylist) :
		listeUnique = []
		for sousListe in listePlaylist :
			if len(sousListe[1]) == 1 :
				listeUnique.append(sousListe)
		return listeUnique

	def __regroupeUnique(self,listeUnique) :
		dictionnaire = {}
		for sousListe in listeUnique :
			RUBRIQUE = list(sousListe[1].keys())[0]
			if RUBRIQUE in dictionnaire :
				tmp = dictionnaire[RUBRIQUE]
				tmp.append(sousListe)
				dictionnaire[RUBRIQUE] = tmp
			else :
				dictionnaire[RUBRIQUE] = [sousListe]
		return(collections.OrderedDict(sorted(dictionnaire.items())))

	def __affichage(self,dictionnaire) :
		for rubrique,playlists in dictionnaire.items() :
			print(rubrique)
			for playlist in playlists :
				print("id "+str(playlist[0])+" :",str(list(playlist[1].values())[0]) + " fois")
			print("\n")

	def selectPlaylists(self) :
		self.__affichage(self.__regroupeUnique(self.__extractUnique(self.__calculPlaylists())))

if __name__ == "__main__":

	myVideo = CanalPlaylist()
	myVideo.selectPlaylists()