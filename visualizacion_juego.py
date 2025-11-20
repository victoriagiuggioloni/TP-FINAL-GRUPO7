import pygame
import random


height = 600
width = 1000
pipe_width = 80
pipe_gap = 200
pipe_speed = 6
fps = 60
pipe_distance = 480

current_distance= 0
average_distance = 0
scroll_speed = 3
speed = scroll_speed

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
        return self.x + self.ancho < 2
    
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

perdio = pygame.image.load('Imágenes/game_over.png')   #texto para cuando no quedan pájaros vivos
game_over = False  


#cambiamos el fondo del juego
#cargamos imagen
fondo = pygame.image.load("Imágenes/fondo.png") #ruta imagen

#Agregando imagenes al juego

#Player
playerImg= pygame.image.load('Imágenes/pajaro.png')
#definimos la posicion del player con sus coordenadas
playerX= 120
playerY= 420

vel_y = 0
gravedad = 0.5

#Postes
tubo_arriba= pygame.image.load('Imágenes/tubo arriba.png')
tubo_abajo= pygame.image.load('Imágenes/TUBO ABAJO.png')

clock = pygame.time.Clock()

#creamos una funcion del player del juego
def dibujar_pajaros(pajaro): #parametros x,y para que podamos definir las posiciones que queramos que tenga el player 
    screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))



tubos = [ Tubo(600, tubo_arriba, tubo_abajo), 
         Tubo(600 + pipe_distance, tubo_arriba, tubo_abajo), 
         Tubo(600 + 2 * pipe_distance, tubo_arriba, tubo_abajo) 
]

from algoritmo import Poblacion
poblacion = Poblacion(None)

#Generamos el loop del juego
running = True
while running:
    screen.blit(fondo, (0,0))
    clock.tick(fps)
    for event in pygame.event.get(): #event es cualquier cosa que sucede dentro del juego
        if event.type == pygame.QUIT:
            running = False #Se termina el loop una vez que el usuario presiona la cruz del juego
        if event.type == pygame.KEYDOWN:  #detecta que apretas una tecla
            if event.key == pygame.K_SPACE:  #detecta que esa tecla es el espacio
                vel_y = -10  #numero negativo mueve el pajaro hacia arriba

    for pajaro in poblacion.pobl:

        #el pajaro apunta hacia el centro del hueco de los tubos
        prox_tubo = tubos[0]
        coordt = (prox_tubo.x, prox_tubo.centro_del_hueco())

        #decidir si aletear
        pajaro.aletear(coordt)

        #actualiza la física del pájaro
        pajaro.actualizar()

        #evita techo, los positivos van para abajo(fuerza de gravedad), los negativos para arria
        if pajaro.y < 0:
            pajaro.y = 0
            pajaro.vy = 0

        #evita el piso, si el numero es mas alto que la pantalla, hace esto
        if pajaro.y > height - playerImg.get_height():
            pajaro.y = height - playerImg.get_height()
            pajaro.vy = 0

        #dibuja el pajaro en la pantalla
        screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))


    #player_hit = pygame.Rect(playerX, playerY, playerImg.get_width(), playerImg.get_height()) #clalculo el hitbox del pajaro

    
    for tubo in list(tubos):
       tubo.mover()
       tubo.dibujar(screen)
      
      #Si el primer tubo salio, crear uno nuevo manteniendo la distancia
    if tubos[0].nuevos_tubos():
       tubos.pop(0) #Eliminamos el tubo que salio
       nueva_x = tubos[-1].x + pipe_distance #posicion basado en el ultimo
       tubos.append(Tubo(nueva_x, tubo_arriba, tubo_abajo))        
       

    #agregamos panel negro a la derecha
    panel_width = 250 #ancho del panel
    panel_x = width - panel_width #lo posicionamos al borde a la derecha

    pygame.draw.rect(screen, (0,0,0), (panel_x,0, panel_width, height))

    
    #titulo del panel
    font_titulo = pygame.font.SysFont("Comic Sans MS", 24, bold = True)
    titulo = font_titulo.render("GA Statistics", True, (250,250,250))
    screen.blit(titulo, (panel_x + 20, 10))
    
    #agregamos texto dentro del panel
    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Generation: ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 60))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Alives: ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 80))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Prev Gen 2min: ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 100))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render(f"Speed: {scroll_speed}X ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 120))

    font = pygame.font.SysFont("Arial", 14)
    current_distance += 1 #se le va sumando la distancia
    texto = font.render(f"Current Distance: {current_distance} ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 160))


    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Best Distance: ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 180))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Avg Distance: ", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 200))

    

    pygame.display.update() #actualizamos el fondo con la imagen

pygame.quit()














