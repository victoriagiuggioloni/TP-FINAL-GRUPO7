import pygame

#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((1024,1024))


#cambiamos nombre del juego
pygame.display.set_caption("Angry Flappy Bird")

#creamos un icono para nuestro juego
icon = pygame.image.load('Imágenes/icono.png')


#cambiamos el fondo del juego
#cargamos imagen
fondo = pygame.image.load("Imágenes/fondo.png") #ruta imagen

#Agregando imagenes al juego
#Agregamos al Player
playerImg= pygame.image.load('Imágenes/angrybird.png')
#definimos la posicion del jugador
playerX= 120
playerY= 425

#creamos una funcion del jugador del juego
def player(): 
    screen.blit(playerImg, (playerX, playerY))

#Generamos el loop del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego
    
    

    screen.blit(fondo,(0,0)) #dibuja el fondo
    pygame.display.set_icon(icon) #actualizamos el icono
    player()
    pygame.display.update() #actualizamos el fondo con la imagen

#TERMINAR ICONO
#FIJARSE PARTE PLAYER













