import pygame
import random


height = 600
width = 1000
pipe_width = 70
pipe_gap = 200
pipe_speed = 6
fps = 60

class Tubo:

    

    def __init__(self, posicion_x, imagen_tubo):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed

        self.imagen_tubo = imagen_tubo
        #altura de tubos
        self.altura_superior = random.randint(50, height - pipe_gap - 50) #altura del tubo de arriba
        self.altura_inferior = self.altura_superior + pipe_gap #donde empieza el tubo de abajo
        #rectangulos 
        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior) #calculo el rectangulo de arriba
        self.rect_abajo = pygame.Rect(self.x, self.altura_inferior, self.ancho, height - self.altura_inferior) 

    def mover(self):
        """Mueve el tubo para la izquierda"""
        self.x -= self.velocidad #más avanza a la derecha, más a la izquierda se mueve el tubo
        self.rect_arriba.x = int(self.x)
        self.rect_abajo.x = int(self.x)

    def dibujar(self, pantalla):
        """Hago que la imagen de los tubos concuerde con el movimiento de pygame"""
        imagen_arriba = pygame.transform.scale(self.imagen_tubo,(self.ancho, self.altura_superior) )
        pantalla.blit(imagen_arriba, (self.x, 0))

        #tubo de abajo
        altura_abajo = height - self.altura_inferior
        imagen_abajo = pygame.transform.scale(self.imagen_tubo,(self.ancho, altura_abajo))
        pantalla.blit(imagen_abajo, (self.x, self.altura_inferior))

        # si querés seguir viendo los rectángulos para debug:
        pygame.draw.rect(pantalla, (0, 255, 0), self.rect_arriba, 2)
        pygame.draw.rect(pantalla, (0, 255, 0), self.rect_abajo, 2)


    def nuevos_tubos(self):
        """Elimina tubos viejos y crea nuevos a la derecha"""
        return self.x + self.ancho < 0
    
    def centro_del_hueco(self):
        """Devuelve la posición y el centro del hueco para que el pájaro sepa dónde apuntar"""
        return self.altura_superior + pipe_gap / 2


#Inicializamos el Juego
pygame.init()

#creamos la pantalla del juego
screen = pygame.display.set_mode((1024,800))


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
posteImg= pygame.image.load('Imágenes/postes.png')
posteX=750
posteY=-350 #pixeles negativos porque la imagen del poste es mas grande que la imagen del fondo

clock = pygame.time.Clock()

#creamos una funcion del player del juego
def player(x,y): #parametros x,y para que podamos definir las posiciones que queramos que tenga el player 
    screen.blit(playerImg, (x, y))



tubos = [ Tubo(width + 50, posteImg), Tubo(width + 180, posteImg)]

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
        tubos[0] = Tubo(width + 180, posteImg)

    pygame.display.update() #actualizamos el fondo con la imagen

pygame.quit()














