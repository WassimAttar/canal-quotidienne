Télécharger automatiquement les émissions quotidiennes de canal.

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [RÉSOLUTION DE PROBLÈME](#resolution-de-probleme)

# DESCRIPTION
**canal-quotidienne** est un petit script qui permet de télécharger automatiquement les émissions quotidiennes de canal plus.

Il suffit de l'éditer pour choisir à quelles émissions s'abonner.

L'historique des émissions déjà téléchargées est sauvegardé.

Le script fait appel à youtube-dl qui doit être préalablement installé.

Pour installer la dernière version de youtube-dl :

    sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/bin/youtube-dl
    sudo chmod 755 /usr/bin/youtube-dl

# INSTALLATION
Télécharger et sauvegarder ce fichier sur votre pc

https://raw.github.com/WassimAttar/canal-quotidienne/master/canal-quotidienne.py

L'éditer pour choisir les émissions à télécharger.

Le lancer en ligne de commande :

    python canal-quotidienne.py

Le téléchargement des émissions commence

# RÉSOLUTION DE PROBLÈME
En cas de problème de téléchargement, télécharger la dernière version de youtube-dl

    sudo youtube-dl -U