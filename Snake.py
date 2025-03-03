import pygame
import sys
import random

pygame.init()

score = 0 #Initialisation du score
width, height = 600, 400 #La taille de la fenêtre
fenetre = pygame.display.set_mode((width, height)) #Crée une fenêtre
pygame.display.set_caption("Snake") #Titre de la fenêtre


vitesseJeu = pygame.time.Clock() #On crée la vitesse de notre jeu

tailleSerpent = 20 #Initialisation de la taille du serpent
vitesseSerpent = 10 #Initialisation de la vitesse du serpent

font = pygame.font.SysFont(None, 30) #Initialisation de la taille de l'écriture

blanc = (255, 255, 255) ##Initialisation des couleurs
rouge = (255, 0, 0)
vert = (0, 255, 0)

def dessinerSerpent(serpent):
    """ Dessine le serpent """
    for pos in serpent:
        pygame.draw.rect(fenetre, vert, pygame.Rect(pos[0], pos[1], tailleSerpent, tailleSerpent))

def dessinerFruit(fruit):
    """ Dessine le fruit """
    pygame.draw.circle(fenetre, rouge, (fruit[0] + tailleSerpent // 2, fruit[1] + tailleSerpent // 2), tailleSerpent // 2)
    
def boucle():
    global score #La variable est utilisée globalement
    gameOver = False
    fermerJeu = False

    serpent = [[width // 2, height // 2], [width // 2, height // 2]]
    serpentDirection = 'UP'

    fruit = [random.randrange(1, (width//tailleSerpent)) * tailleSerpent,
            random.randrange(1, (height//tailleSerpent)) * tailleSerpent]

    while not gameOver:

        while fermerJeu:
            #Affiche l'écran de fin de jeu
            fenetre.fill(blanc)
            message = font.render("Appuyez sur Q pour quitter ou sur C pour rejouer", True, rouge)
            fenetre.blit(message, [width / 10, height / 2])
            texteScore = font.render("Score: " + str(score), True, rouge)
            fenetre.blit(texteScore, [width / 2.5, height / 3])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        fermerJeu = False
                    elif event.key == pygame.K_c:
                        score = 0  #Réinitialise le score
                        boucle()
                        
        #La direction du serpent est mise à jour en fonction des touches du clavier pressées par l'utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not serpentDirection == 'RIGHT':
                    serpentDirection = 'LEFT'
                elif event.key == pygame.K_RIGHT and not serpentDirection == 'LEFT':
                    serpentDirection = 'RIGHT'
                elif event.key == pygame.K_UP and not serpentDirection == 'DOWN':
                    serpentDirection = 'UP'
                elif event.key == pygame.K_DOWN and not serpentDirection == 'UP':
                    serpentDirection = 'DOWN'

        #Met à jour la position du serpent en fonction de la direction
        if serpentDirection == 'UP':
            serpent[0][1] -= tailleSerpent
        elif serpentDirection == 'DOWN':
            serpent[0][1] += tailleSerpent
        elif serpentDirection == 'LEFT':
            serpent[0][0] -= tailleSerpent
        elif serpentDirection == 'RIGHT':
            serpent[0][0] += tailleSerpent

        #Vérifie les collisions avec les bords de l'écran
        if serpent[0][0] >= width or serpent[0][0] < 0 or serpent[0][1] >= height or serpent[0][1] < 0:
            fermerJeu = True

        #Vérifie les collisions avec le corps du serpent
        for segment in serpent[1:]:
            if segment == serpent[0]:
                fermerJeu = True

        #Vérifie la collision avec le fruit
        if serpent[0] == fruit:
            score += 1
            fruit = [random.randrange(1, (width//tailleSerpent)) * tailleSerpent,
                    random.randrange(1, (height//tailleSerpent)) * tailleSerpent]
            serpent.append([0, 0])

        #Déplace le corps du serpent
        for i in range(len(serpent) - 1, 0, -1):
            serpent[i] = serpent[i - 1][:]

        fenetre.fill(blanc)
        #On dessine le serpent et le fruit
        dessinerSerpent(serpent)
        dessinerFruit(fruit)

        pygame.display.flip()
        vitesseJeu.tick(vitesseSerpent)

    pygame.quit()
    sys.exit()

boucle()
