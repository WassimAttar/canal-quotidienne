# coding: utf-8

import os, time, xml.dom.minidom, socket, threading

try:
	import urllib.request as compat_urllib_request
except ImportError:  # Python 2
	import urllib2 as compat_urllib_request

try:
	import queue as compat_queue
except ImportError:  # Python 2
	import Queue as compat_queue


homedir = os.path.expanduser('~')

# Dossier ou les playlists sont sauvegardées
playlistdir = homedir + "/dev/canal-quotidienne/playlists/"

class CanalScan :

	__NBWORKERS = 10
	__MAXPLAYLIST = 4000

	# URL de toutes les vidéos d'une émission donnée.
	__urlXmlMea = 'http://service.canal-plus.com/video/rest/getMEAs/cplus/{}'

	def __init__(self):
		pass

	def __parseXml(self,xmldoc):
		meas = xmldoc.getElementsByTagName('MEA')
		if len(meas)>0 :
			return True
		else :
			return False

	def __downloadXml(self,url):
		downloadTries = 0
		xmlFile = None
		while xmlFile is None :
			try:
				xmlFile = compat_urllib_request.urlopen(url,timeout = 3).read()
			except (compat_urllib_request.URLError, socket.timeout) as err:
				if downloadTries > 3:
					print("Problème de téléchargement, réessayez plus tard")
					exit()
				else:
					downloadTries += 1
					print("Essai n°"+str(downloadTries))
					time.sleep(3)
		return xmlFile

	def __parseXmlMea(self,xmlFile) :
		return xml.dom.minidom.parseString(xmlFile)

	def __savePlaylist(self,xmlFile,codePlaylist):
		playlistFile = playlistdir+str(codePlaylist)+".xml"
		file = open(playlistFile, 'wb')
		file.write(xmlFile)
		file.close()

	def __geturlXmlMea(self,code):
		return CanalScan.__urlXmlMea.format(code)

	def __downloadPlaylist(self,codePlaylist):
		print("playlist "+str(codePlaylist))
		urlXmlMea = self.__geturlXmlMea(codePlaylist)
		xmlMea = self.__downloadXml(urlXmlMea)
		mea = self.__parseXmlMea(xmlMea)
		if self.__parseXml(mea) :
			self.__savePlaylist(xmlMea,codePlaylist)


	def __worker(self):
		while True :
			codePlaylist = self.__q.get()
			self.__downloadPlaylist(codePlaylist)
			self.__q.task_done()

	def downloadPlaylists(self):
		self.__q = compat_queue.Queue()
		for i in list(range(CanalScan.__NBWORKERS)):
			t=threading.Thread(target=self.__worker)
			t.daemon = True
			t.start()
		for codePlaylist in list(range(0,CanalScan.__MAXPLAYLIST)) :
			self.__q.put(codePlaylist)
		self.__q.join()


if __name__ == "__main__":

	myVideo = CanalScan()
	myVideo.downloadPlaylists()