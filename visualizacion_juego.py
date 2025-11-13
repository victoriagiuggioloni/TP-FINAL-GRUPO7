import pygame

#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((1024,800))


#cambiamos nombre del juego
pygame.display.set_caption("Angry Flappy Bird")

#creamos un icono para nuestro juego
icon = pygame.image.load('Imágenes/pajaro_icono.png')


#cambiamos el fondo del juego
#cargamos imagen
fondo = pygame.image.load("Imágenes/fondo.png") #ruta imagen

#Agregando imagenes al juego

#Player
playerImg= pygame.image.load('Imágenes/pajaro.png')
#definimos la posicion del player con sus coordenadas
playerX= 120
playerY= 420

#Postes
posteImg= pygame.image.load('Imágenes/postes.png')
posteX=750
posteY=-350 #pixeles negativos porque la imagen del poste es mas grande que la imagen del fondo


#creamos una funcion del player del juego
def player(x,y): #parametros x,y para que podamos definir las posiciones que queramos que tenga el player 
    screen.blit(playerImg, (x, y))

def poste(x,y):
    screen.blit(posteImg,(x,y))

#Generamos el loop del juego
running = True
while running:
    for event in pygame.event.get(): #event es cualquier cosa que sucede dentro del juego
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego
    
    screen.blit(fondo,(0,0)) #dibuja el fondo

    pygame.display.set_icon(icon) #actualizamos el icono
    player(playerX, playerY) #llamamos la funcion del jugador asi nos aparece en el juego
    poste(posteX, posteY) #llamamos funcion poste
    pygame.display.update() #actualizamos el fondo con la imagen
















