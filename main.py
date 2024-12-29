import pygame
import random
import time

pygame.init()

screen_width = 700
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Block Blast")

clock = pygame.time.Clock()

# Couleurs
GRIS_FONCE = (100, 100, 100)
GRIS_MOYEN = (180, 180, 180)
ROUGE = (255, 0, 0)

couleurs = [
    (135, 206, 250),
    (255, 127, 80),
    (244, 164, 96),
    (152, 255, 152)
]

# Variables du jeu
FPS = 60
rectangle_rejouer = pygame.Rect(265, 280, 200, 40)
ombre_rect = pygame.Rect(260, 285, 200, 41)

class Block:

    def __init__(self):
        self.fig_futur = random.randint(1, 5)
        self.dir_futur = random.randint(1, 4)
        self.figure = self.fig_futur
        self.direction = self.dir_futur
        
        self.x_futur = 575
        self.y_futur = 100
        
        self.cote = 25
        self.score = 0
        self.commencement = False
        self.run = True
        self.futur = True
        self.rejouer = False
        #initialiser la font
        self.font = pygame.font.SysFont(None, 36)
        #textes
        self.game_over_text = self.font.render("GAME OVER", True, (0, 0, 0))
        self.replay_text = self.font.render("REJOUER??", True, (0, 0, 0))
        self.debut_text = self.font.render("POUR COMMENCER TAPER", True, (0, 0, 0))
        self.moitie = self.font.render("LA BARRE D'ESPACE", True, (0, 0, 0))

        #Images
        self.img = pygame.image.load("assets/bg12.jpg")
        self.img2 = pygame.image.load("assets/bg9.jpg")
        self.bg = pygame.transform.scale(self.img, (700, 600))

        #Sons
        self.click_song = pygame.mixer.Sound("assets/sounds/click.ogg")
        self.depot_song = pygame.mixer.Sound("assets/sounds/depot.ogg")
        self.game_over_song = pygame.mixer.Sound("assets/sounds/game_over.ogg")

        self.rectangles_pos_sur_sol = []
        self.rectangles_sur_sol = []
        self.initialisation()

    def initialisation(self):
        self.y_depart = 0
        self.x_depart = 250
        self.timer = 1
        self.descente_rapide = False
        self.aligne = False
        self.position_alignement = -1
        self.rectangle_pos = []
        self.rectangles = []
        self.quadrillage = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    # Définition de la fonction pour calculer les positions des rectangles
    def calculer_positions_rectangles(self, x, y, in_fig, in_dir):

        if in_fig == 1:
            if in_dir == 1:
                return [(x, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x + (2 * self.cote), y, self.cote, self.cote)]
            elif in_dir == 2:
                return [(x, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x, y + (2 * self.cote), self.cote, self.cote)]
            elif in_dir == 3:
                return [(x, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x - (2 * self.cote), y, self.cote, self.cote)]
            elif in_dir == 4:
                return [(x, y, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x, y - (2 * self.cote), self.cote, self.cote)]
        elif in_fig == 2:
            if in_dir == 1:
                return [(x, y, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote)]
            elif in_dir == 2:
                return [(x, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote)]
            elif in_dir == 3:
                return [(x, y, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote)]
            elif in_dir == 4:
                return [(x, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote)]
        elif in_fig == 3:
            if in_dir == 1:
                return [(x, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x - self.cote, y - self.cote, self.cote, self.cote)]
            elif in_dir == 2:
                return [(x, y, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x + self.cote, y - self.cote, self.cote, self.cote)]
            elif in_dir == 3:
                return [(x, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x + self.cote, y + self.cote, self.cote, self.cote)]
            elif in_dir == 4:
                return [(x, y, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x - self.cote, y + self.cote, self.cote, self.cote)]
        elif in_fig == 4:
            if in_dir == 1 or in_dir == 3:
                return [(x, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x, y + self.cote, self.cote, self.cote), (x, y + (2 * self.cote), self.cote, self.cote)]
            elif in_dir == 2 or in_dir == 4:
                return [(x, y, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x + (2 * self.cote), y, self.cote, self.cote), (x + self.cote, y, self.cote, self.cote)]
        elif in_fig == 5:
            if in_dir == 1 or in_dir == 2 or in_dir == 3 or in_dir == 4:
                return [(x, y, self.cote, self.cote), (x, y - self.cote, self.cote, self.cote), (x - self.cote, y, self.cote, self.cote), (x - self.cote, y - self.cote, self.cote, self.cote)]

    #Fonction qui dessine tout sur l'écran lorsque le jeu est encours
    def dessiner_rectangle(self):

        #screen.fill(GRIS_FONCE)


        # Dessiner les blocs qui sont au sol
        couleur_de_base = 0
        for rectangle in self.rectangles_pos_sur_sol:
            #attribuer les couleurs
            if couleur_de_base > 3:
                couleur_de_base = 0
            pygame.draw.rect(screen, couleurs[couleur_de_base], rectangle)
            couleur_de_base += 1


        # Nouveau bloc
        self.rectangle_pos = self.calculer_positions_rectangles(self.x_depart, self.y_depart, self.figure, self.direction)

        # Dessiner le bloc descendant
        for i, rectangle in enumerate(self.rectangle_pos):
            pygame.draw.rect(screen, couleurs[i], rectangle)

        #Dessiner les ligne pour séparer les elements du bloc descendant
        for x in range(21):
            pygame.draw.line(screen, GRIS_FONCE, (x * self.cote, 0), (x * self.cote, screen_height), 1)
        for y in range(25):
            pygame.draw.line(screen, GRIS_FONCE, (0, y * self.cote), (screen_width, y * self.cote), 1)

        pygame.draw.rect(screen, (0, 0, 0), (500, 0, 200, screen_height))

        self.futur_block()
        self.afficher_textes(pygame.font.SysFont(None, 30).render("FUTUR BLOCK", True, (255, 255, 255)), (515, 75))

        #Afficher le score à l'écran
        self.score_rect = pygame.Rect(0, 0, screen_width, 50)
        pygame.draw.rect(screen, (32, 32, 32), self.score_rect)
        self.score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.afficher_textes(self.score_text, (10, 10))

        #Afficher la description 
        self.afficher_textes(pygame.font.SysFont("arial", 10).render("CREE PAR RUTETE", True, (200, 200, 200)), (615, 30))
        self.afficher_textes(pygame.font.SysFont("arial", 10).render("BLOCK BLAST", True, (200, 200, 200)), (615, 10))

    #La fonction qui vérifie si le bloc peut continuer à descendre
    def descente(self):

        if self.figure == 1:
            if self.direction == 2:
                if self.y_depart < screen_height - (3 * self.cote):
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            elif self.direction == 1:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            elif self.direction == 4:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            elif self.direction == 3:
                if self.y_depart < screen_height - (2 * self.cote):
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
        elif self.figure == 2:
            if self.direction == 1:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            else:
                if self.y_depart < screen_height - (2 * self.cote):
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
        elif self.figure == 3:
            if self.direction == 2:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            else:
                if self.y_depart < screen_height - (2 * self.cote):
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
        elif self.figure == 4:
            if self.direction == 1 or self.direction == 3:
                if self.y_depart < screen_height - (3 * self.cote):
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
            else:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
        elif self.figure == 5:
            if self.direction == 1 or self.direction == 2 or self.direction == 3 or self.direction == 4:
                if self.y_depart < screen_height - self.cote:
                    if not self.verifier_collision(self.x_depart, self.y_depart + self.cote):
                        return True
        
        return False

    #La fonction qui gère tout
    def deplacement_bloc_descendant(self):

        #remplir la liste du quadrillage
        self.quadrilleur(self.rectangles_pos_sur_sol)

        #Dessiner sur l'écran
        self.dessiner_rectangle()

        # Définition de la vitesse de descente des blocs
        if self.timer > 30:
            self.timer = 1
            if self.descente():
                #Faire descendre le bloc
                self.y_depart += self.cote
                self.futur = False
            else:
                self.depot_song.play()
                #Créer des rectangles avec les positions dans la liste du bloc
                for rectangle in self.rectangle_pos:
                    self.rectangles = pygame.Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])
                    self.rectangles_pos_sur_sol.append(self.rectangles)
                    self.rectangles = []
                #Vérification si il y'a des blocs alignés ou pas
                self.position_alignement = self.alignement()

                if self.aligne:
                    #Retirer les blocs alignés
                    self.retirer()
                    #Mettre à jour le score
                    self.score += 20 * len(self.position_alignement)
                    time.sleep(0.550) #on attend 50 millisecondes
                #Initialiser le programme
                self.figure = self.fig_futur
                self.direction = self.dir_futur
                self.futur = True
                self.initialisation()
        #Activer la descente rapide
        elif self.descente_rapide:
            self.timer += 15
        else:
            self.timer += 1

    #Fontion qui retire les blocs lorsqu'ils sont alignés
    def retirer(self):

        #Variable qui stocke les blocs à supprimer
        to_remove = [rect for rect in self.rectangles_pos_sur_sol if (rect.centery // self.cote) in self.position_alignement]

        #Retirer les blocs
        for rect in to_remove:
            self.rectangles_pos_sur_sol.remove(rect)

        #Mettre à jour la nouvelle position des blocs restant
        for rect in self.rectangles_pos_sur_sol:
            for element in self.position_alignement:
                if rect.centery // self.cote < element:
                    rect.y += self.cote

    #La fonction qui verifie les collisions entre le bloc descendant et les blocs au sol
    def verifier_collision(self, x, y):

        #Variable qui stocke la position future du bloc descendant
        future_rectangles = self.calculer_positions_rectangles(x, y, self.figure, self.direction)

        #Gestion des collisions du bloc futur aux blocs au sol
        for rect in future_rectangles:
            for rect2 in self.rectangles_pos_sur_sol:
                if pygame.Rect(rect).colliderect(rect2):
                    return True
        return False
    
    #La fonction qui remplit la liste qui contient les blocs de l'écran
    def quadrilleur(self, groupe_rectangle):

        for rect in groupe_rectangle:
            x = rect.centerx // self.cote
            y = rect.centery// self.cote
            self.quadrillage[y][x] = 1

    #La fonction qui gère si les blocs sont alignés ou pas
    def alignement(self):

        #Variable contenant les positions des blocs alignés
        liste = []

        for y in range(24):
            somme_y = 0
            for x in range (19):
                somme_y += self.quadrillage[y][x]

            #Verification si les blocs sont alignés
            if somme_y >= 19:
                self.aligne = True
                liste.append(y)
        return liste
    
    #La fontion qui regarde si le joueur a perdu ou pas
    def game_over(self):
        y = 5
        for x in range(19):
            if self.quadrillage[y][x] == 1:
                self.rejouer = True
                self.game_over_song.play()
                return True
        return False

    #Fonction qui affiche les textes
    def afficher_textes(self, text, position):
        # Dessiner le texte sur l'écran
        screen.blit(text, position)

    #Fonction qui dessine le futur block
    def futur_block(self):
        if self.futur:
            self.fig_futur = random.randint(1, 5)
            self.dir_futur = random.randint(1, 4)
        x_futur = 575
        y_futur = 175
        bloc_futur = self.calculer_positions_rectangles(x_futur, y_futur, self.fig_futur, self.dir_futur)
        for i, rectangle in enumerate(bloc_futur):
            pygame.draw.rect(screen, couleurs[i], rectangle)

    #Fonction principale
    def jeu(self):
        #Vérification si le joueur a perdu ou non
        if self.game_over() and self.rejouer:
            screen.fill(GRIS_FONCE)
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (10, 10, 10), ombre_rect)
            pygame.draw.rect(screen, (255, 255, 255), rectangle_rejouer)
            self.afficher_textes(self.game_over_text, (285, 250))
            self.afficher_textes(self.replay_text, (300, 285))
            self.afficher_textes(pygame.font.SysFont("arial", 10).render("CREE PAR RUTETE", True, (0, 0, 0)), (615, 585))
            self.afficher_textes(pygame.font.SysFont("arial", 25).render(f"VOTRE SCORE EST : {self.score}", True, (0, 0, 0)), (250, 350))
        
        #Afficher le texte lorsque le joueur a perdu
        elif not self.commencement:
            screen.fill(GRIS_FONCE)
            screen.blit(self.bg, (0, 0))
            self.afficher_textes(self.debut_text, (200, 250))
            self.afficher_textes(self.moitie, (230, 285))
            self.afficher_textes(pygame.font.SysFont("arial", 10).render("CREE PAR RUTETE", True, (0, 0, 0)), (615, 585))

        #Le jeu commence
        else:
            screen.blit(pygame.transform.scale(self.img, (700, 600)), (0, 0))
            block.deplacement_bloc_descendant()

#Créer un block
block = Block()

while block.run:
    clock.tick(FPS)

    #Appeler la fonction principale
    block.jeu()

    #Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Quitter le jeu
            block.run = False

        #Toucher le clavier
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and block.y_depart < screen_height - block.cote:
                if block.direction > 3:
                    block.direction = 1
                else:
                    block.direction += 1
            elif event.key == pygame.K_SPACE:
                block.commencement = True
            elif event.key == pygame.K_LEFT and block.y_depart < screen_height - block.cote:
                block.x_depart -= block.cote
            elif event.key == pygame.K_RIGHT and block.y_depart < screen_height - block.cote:
                block.x_depart += block.cote
            elif event.key == pygame.K_DOWN:
                block.descente_rapide = True

        #Click de la souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if rectangle_rejouer.collidepoint(mouse_pos):
                block.click_song.play()
                print("yes")
                #Initialiser le jeu
                block.initialisation()
                block.score = 0
                block.rectangles_pos_sur_sol = []
                block.commencement = True

    pygame.display.update()

pygame.quit()