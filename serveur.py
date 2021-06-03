import socket
from _thread import *
import pickle
from jeu import Jeu

"""serveur et port """
server = "192.168.1.16"
port = 5556
"""le type de connection AF_INET ,sock stream = tcp socket"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""on lie notre port et à notre serveur """
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
"""ouvre les ports pour avoir de multiples clients qui puissent se connecter """
"""on a initialisé 2 personnes qui peuvent se connecter au serveur"""
s.listen(2)
print("En attente d'une connexion, Serveur Lancé")

"""va stocker l'adresse ip de notre client et idcount pour set une id pour chaque partie """
connected = set()
jeux = {}
idCount = 0

"""notre fonction de traitement"""
def threaded_client(conn, p, jeuId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    """va envoyer get pour avoir la partie , reset pour redémarrer la partie, move pour connaitre le coup du joueur"""
    while True:
        try:
            data = conn.recv(4096).decode()
            """on va recevoir des données de connection plus les bits sont élévé plus le temps de réception vont être élévé"""

            """pour vérifier si l'id est toujours la car si 1 client se deco, la partie est supprimée"""
            if jeuId in jeux:
                game = jeux[jeuId]

                if not data:
                    """si on essaie d'avoir des informations du client on va le déconnecter"""
                    break

                else:
                    """on vérifie si on a un get ,reset et un move"""
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
                    """envoyer à notre client et utiliser les infos pour jouer"""
            else:
                break
        except:
            break
    """pour fermer la partie"""
    print("Connexion perdue")
    try:
        """supprime la partie"""
        del jeux[jeuId]
        print("Le jeu se ferme", jeuId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    """va accepter les connexions """
    conn, addr = s.accept()
    print("Connecté à:", addr)
    """poursuivre combien de personnes sont connectées à notre serveur"""
    idCount += 1
    p = 0
    """toutes les 2 personnes connectées on va augmenter notre gameID d'un"""
    gameId = (idCount - 1)//2
    """si il y'a une personne en plus par exemple, une nouvelle devra être créée"""
    if idCount % 2 == 1:
        jeux[gameId] = Jeu(gameId)
        print("Création d'une nouvelle partie")
    else:
        """si une personne se connecte et qu'une partie est deja existante elle va se connecter à celle-ci"""
        jeux[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
    """pour avoir plusieurs connexion  et ne pas attendre que threated_client finisse de s'executer pour avoir une nouvelle connexion """