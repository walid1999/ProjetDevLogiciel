class Jeu:
    """id des joueurs"""
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
    """on récupère l'info du joueur son choix"""
    def get_player_move(self, p):
        return self.moves[p]
    """mets à jour les choix avec les mouvement de ces joueurs dans la list moves"""
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    """pour savoir si nos joueurs sont connecté """
    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went
    """règle du jeu pour savoir qui gagne"""
    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "P" and p2 == "C":
            winner = 0
        elif p1 == "C" and p2 == "P":
            winner = 1
        elif p1 == "F" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "F":
            winner = 1
        elif p1 == "C" and p2 == "F":
            winner = 0
        elif p1 == "F" and p2 == "C":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False