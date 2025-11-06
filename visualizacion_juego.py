import pygame

#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((1024,1024))


#cambiamos nombre del juego
pygame.display.set_caption("Angry Flappy Bird")

#creamos un icono para nuestro juego
icon = pygame.image.load('icono.png')
pygame.display.set_icon(icon)

#Generamos el loop del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego

#cambiamos el fondo del juego
#fondo = pygame.image.load()







