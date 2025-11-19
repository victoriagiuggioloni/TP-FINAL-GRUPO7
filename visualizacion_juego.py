import pygame
import random


height = 600
width = 1000
pipe_width = 140
pipe_gap = 200
pipe_speed = 6
fps = 60
pipe_distance = 250


class Tubo:

    

    def __init__(self, posicion_x, imagen_arriba, imagen_abajo):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed

        self.imagen_arriba_original = imagen_arriba
        self.imagen_abajo_original  = imagen_abajo
        #altura de tubos
        self.altura_superior = random.randint(110, height - pipe_gap - 110) #altura del tubo de arriba
        self.altura_inferior = self.altura_superior + pipe_gap #donde empieza el tubo de abajo
        #rectangulos 
        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior) #calculo el rectangulo de arriba
        self.rect_abajo = pygame.Rect(self.x, self.altura_inferior, self.ancho, height - self.altura_inferior) 

    def mover(self):
        """Mueve el tubo para la izquierda"""
        self.x -= self.velocidad #más avanza a la derecha, más a la izquierda se mueve el tubo3
        self.rect_arriba.x = int(self.x)
        self.rect_abajo.x = int(self.x)

    def dibujar(self, pantalla):
        """Hago que la imagen de los tubos concuerde con el movimiento de pygame"""
        imagen_arriba = pygame.transform.scale(self.imagen_arriba_original,(self.ancho, self.altura_superior) )
        pantalla.blit(imagen_arriba, (self.x, 0))

        #tubo de abajo
        altura_abajo = height - self.altura_inferior
        imagen_abajo = pygame.transform.scale(self.imagen_abajo_original,(self.ancho, altura_abajo))
        pantalla.blit(imagen_abajo, (self.x, self.altura_inferior))

        
        #pygame.draw.rect(pantalla, (0, 255, 0), self.rect_arriba, 2)
        #pygame.draw.rect(pantalla, (0, 255, 0), self.rect_abajo, 2)


    def nuevos_tubos(self):
        """Elimina tubos viejos y crea nuevos a la derecha"""
        return self.x + self.ancho < 0
    
    def centro_del_hueco(self):
        """Devuelve la posición y el centro del hueco para que el pájaro sepa dónde apuntar"""
        return self.altura_superior + pipe_gap / 2


#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((width,height))


#cambiamos nombre del juego
pygame.display.set_caption("Angry Flappy Bird")

#creamos un icono para nuestro juego
icon = pygame.image.load('Imágenes/pajaro_icono.png')
pygame.display.set_icon(icon) #actualizamos el icono


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
tubo_arriba= pygame.image.load('Imágenes/tubo arriba.png')
tubo_abajo= pygame.image.load('Imágenes/TUBO ABAJO.png')

clock = pygame.time.Clock()

#creamos una funcion del player del juego
def player(x,y): #parametros x,y para que podamos definir las posiciones que queramos que tenga el player 
    screen.blit(playerImg, (x, y))



tubos = [ Tubo(600, tubo_arriba, tubo_abajo), Tubo(600 + pipe_distance, tubo_arriba, tubo_abajo), Tubo(600 + 2 * pipe_distance, tubo_arriba, tubo_abajo) ]

#Generamos el loop del juego
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get(): #event es cualquier cosa que sucede dentro del juego
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego
    
    screen.blit(fondo,(0,0)) #dibuja el fondo

    player(playerX, playerY) #llamamos la funcion del jugador asi nos aparece en el juego
    
    for tubo in tubos:
        tubo.mover()
        tubo.dibujar(screen)
        if tubos[0].nuevos_tubos():
            # ahora el tubo[1] pasa a ser el de adelante
            tubos[0] = tubos[2]

            # creamos un nuevo tubo detrás, manteniendo la misma distancia
            nueva_x = tubos[0].x + pipe_distance
            tubos[2] = Tubo(nueva_x, tubo_arriba, tubo_abajo)

    pygame.display.update() #actualizamos el fondo con la imagen

pygame.quit()














