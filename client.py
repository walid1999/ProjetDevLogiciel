import pygame
from reseau import Reseau

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")



class Bouton:
    """Bouton :va être appelé automatiquement après qu’un objet ai été créé c'est initialisateur """
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        """"""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        """pour savoir quand on clique sur notre bouton"""
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    """"fond"""
    win.fill((0,0,0))

    """si le joueur est connecté et qu'il n'y a pas de partie, il attend un joueur"""
    if not(game.connected()):
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("En attente d'un autre joueur...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    else:
        """si les 2 joueurs sont connectés, l'écran du jeu va être affiché """
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Ton choix", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Adversaire", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        """pour montrer le coup de chaque joueur"""
        if game.bothWent():
            text1 = font.render(move1, 1, (255, 0, 0))
            text2 = font.render(move2, 1, (255, 0, 0))
        else:
            """le joueur 1"""
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,0,0))
            elif game.p1Went:
                text1 = font.render("Choix fait", 1, (255, 0, 0))
            else:
                text1 = font.render("En attente", 1, (255, 0, 0))

            """le joueur 2"""
            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,0,0))
            elif game.p2Went:
                text2 = font.render("Choix fait", 1, (255, 0, 0))
            else:
                text2 = font.render("En attente", 1, (255, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

"""définition des boutons pierre feuille et ciseaux"""
btns = [Bouton("Pierre", 50, 500, (0, 0, 255)), Bouton("Ciseaux", 250, 500, (255, 0, 0)), Bouton("Feuille", 450, 500, (0, 255, 0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Reseau()
    player = int(n.getP())
    print("Tu es le joueur", player)

    while run:
        clock.tick(60)
        """demande au serveur de nous envoyer la game"""
        try:
            game = n.send("get")
            """si il n'y a pas de réponse ça veut dire que la partie n'existe pas """
        except:
            run = False
            print("Aucune partie trouvée")
            break

        if game.bothWent():
            """on met à jour la page pour pouvoir jouer les prochain round """
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Aucune partie trouvée")
                break


            """résultat du match , pour savoir quel joueur à gagner"""
            font = pygame.font.SysFont("Arial", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Tu as gagné !", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Egalité", 1, (255,0,0))
            else:
                text = font.render("Tu as perdu", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        """"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            """pour verifier s'il utilise bien le clique"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        """pour ne pas pouvoir jouer avant que l'autre joueur se connecte"""
                        if player == 0:
                            """envoie au réseau notre move soit juste le text de ce dernier"""
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)
"""menu d'avant jeu"""
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Click pour jouer", 1, (255,0,0))
        win.blit(text, (200,300))
        pygame.display.update()
        """si le joueur clique quelque part on va appeler la fonction main"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
