import socket
import pickle


class Reseau:
    """on définit les ports,on définit encore notre type de connexion"""
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "176.144.221.9"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()
        """on va avoir une id pour savoir si c'est la client 1 ou 2"""

    def getP(self):
        return self.p
    """quand un client se connecte on va envoyer des informations à notre client encodé et va le decodé  """
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
