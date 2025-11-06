import os
import pygame

#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((1024,1024))


#cambiamos nombre del juego
pygame.display.set_caption("Angry Flappy Bird")

#obtenemos ruta del archivo del icono
base_path = os.path.dirname(__file__)
icon_path = os.path.join(base_path, "bird.png.png")

#creamos un icono para nuestro juego
icon = pygame.image.load(icon_path)
#cambiamos tamano de icono
icono = pygame.transform.scale(icon, (32,32))
pygame.display.set_icon(icono)




#Generamos el loop del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego

#cambiamos el fondo del juego
#fondo = pygame.image.load()







