import pygame
from pygame.locals import *
import random
import math

# variables qui servent dans differentes parties du jeux
clock = pygame.time.Clock()
start = False
menu = True
wait = True
result = False
money = 1000
mise = 0
first = 0
nombre = 0
rnd = 0
turn = False
angle = 0
x = -0.1
speed = True
white = (255,255,255)

#listes des numeros et des angles de la roue (ne fonctionne pas)
number_wheel = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
angle_number_wheel = []
for i in range(len(number_wheel)):
  angle_number_wheel.append(i*(360/37)) #37 nombre sur 360 degrées


pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('CASINO')

#initialiser et afficher ecran
background = pygame.Surface(screen.get_size())
background = background.convert()
background = pygame.image.load("data/bg2.jpg").convert()
ecran = pygame.Surface(screen.get_size())
ecran = ecran.convert()
screen.blit(background, (0, 0))
pygame.display.flip()

#afficher la roue
roulette = pygame.image.load("data/roulette.png")
wheel = roulette
orig_wheel = roulette
rect = roulette.get_rect(center=(250, 250))
angle = 0

def txt(texte,taille,hauteur=0,color=white): #fonction qui sert a afficher le texte
  font = pygame.font.Font(None, taille)
  text = font.render(texte, 1, color)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.centery = background.get_rect().centery + hauteur
  screen.blit(text, textpos)

def clear():
  screen.blit(background, (0, 0))

def wait(wait): #attendre sans bloquer la fenetre sur windows ou passer l'attente en appuyant sur espace
  for i in range(int(wait)):
    pygame.time.wait(10)
    try:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
          pygame.quit()
          quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
          return 0
    except:
      pass

def rotate(image, rect, angle): #faire tourner une image (la roue)
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect

def loose():
  clear()
  txt("Tu as perdu !!!", 50, 0,(255,128,0))
  pygame.display.flip()
  wait(500)
  pygame.quit()
  quit()

def f(x): #fonction qui sert a definir la vitesse de rotation de la roue
  return x**2

#---------------------------------------------------------------------- Boucle du jeux
while True:

  #detecter les touches
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      quit()
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.quit()
        quit()
        break
      if event.key == K_RETURN:
        start = True
        angle = 0
      if event.key == K_SPACE and start == True:
        first = 3
        turn = True
  
  #demarrer la partie
  if start == True:
    clear()
    txt("Argent : "+str(money)+"€  ,     Mise : "+str(mise)+"€  ,     Numéro : "+str(nombre),30,235)

    if turn == False and angle == 0 and first == 0: #faire choisir la mise et le nombre
      txt("Regarde la console !",50,-200)
      first = 1
    elif turn == False and angle == 0 and first == 1: #choix dans la console
      first = 2
      mise = int(input("\n\nCombien veut-tu miser ("+str(money)+"€ disponible) \n> "))
      money -= mise
      if money < 0:
        loose()
      while not nombre >= 1 and nombre <= 36:
        nombre = int(input("\nChoisit un nombre entre 1 et 36\n> "))
        if nombre > 36:
          print("Ton nombre est trop grand !")
        elif nombre < 0 :
          print("Ton nombre est trop petit !")
      print("\nTu peux retourner sur le jeux !\n")

    if first == 2: #menu pour demander de faire tourner la roue
      txt("Appuis sur ESPACE", 50, -230)
      txt("pour faire tourner la roue", 40, -200)
      xspeed = random.randint(-15,-5) #vitesse de la roue

    if turn == True: #tourner la roue
      txt("La roue tourne !!!", 60, -200)
      if speed == False: #speed a False sert a faire diminuer la vitesse de la roue
        x +=0.03
      elif speed == True: #speed a True sert a augmenter la vitesse de la roue (démarage)
        if x > -10:
          x -= 0.3
        else:
          x = xspeed
          speed = False
          
      angle += f(x)
      if x > 0: #quans la vitesse de la roue est a 0...
        degrees = angle%360
        for index,rotation in enumerate(angle_number_wheel): #...on essayer de detecter le nombre affiché grace a l'angle (mais ne fonctionne pas)
          if degrees > rotation-5 and degrees < rotation+5:
            rnd = number_wheel.index(index)
              
        turn = False
        result = True
        speed = True
        x = -0.1
        angle = 0
      turn_wheel, rect = rotate(orig_wheel, rect, angle)
      screen.blit(turn_wheel, (rect[0],rect[1]+20))
    
    if result == True: #si la roue a terminé de tourner
      clear()
      rnd = random.randint(0,36)#on génere un nombre car la roue ne fonctionne pas tres bien
      txt("Et le resultat est:", 50, -200)
      pygame.display.flip()
      wait(100)
      txt(" "+str(rnd)+" !!!", 60, -150)
      pygame.display.flip()
      wait(100)
      if rnd == nombre: #afficher message en fonction du nombre aléatoire
        txt("TU AS GAGNÉ !!!!", 70,0,(20,255,20))
        pygame.display.flip()
        money+=mise*3
      elif nombre%2==rnd%2:
        money+=math.ceil(mise/2)
        txt("PERDU",60,0,(255,128,0))
        pygame.display.flip()
        txt("mais comme ton numero est de la meme couleur,",30,50)
        pygame.display.flip()
        txt ("tu gagne 50% de ta mise",30,80)
        pygame.display.flip()
      else:
        txt("TU AS PERDU !!!!", 70,0,(255,128,0))
        pygame.display.flip()
      txt("Tu avais choisit "+str(nombre),40,200)
      nombre = 0
      mise = 0
      pygame.display.flip()
      wait(100)
      txt("Argent : "+str(money)+"€  ,     Mise : "+str(mise)+"€  ,     Numéro : "+str(nombre),30,235)
      pygame.display.flip()
      wait(100)
      txt("Appui sur ESPACE pour continuer",30,-235,(0,150,255))
      pygame.display.flip()
      wait(3000)
      result = False
      angle = 0
      first = 0
      if money == 0:
        loose()

  #sinon afficher le menu
  else:
    clear()
    angle += 1
    turn_wheel, rect = rotate(orig_wheel, rect, angle)
    screen.blit(turn_wheel, (rect[0],rect[1]+20))
    txt("Appuis sur ENTREE pour jouer !", 40, -220)
    txt("CASINO", 150)
    txt("BONSOIR !!!", 50,60)
    txt("BIENVENUE POUR PERDRE DE L'ARGENT !!!!", 32,235)

  pygame.display.flip()
  clock.tick(30)
