import pygame
import random
from algoritmo import Poblacion
from funciones import *

height = 600
width = 1000
pipe_width = 80
pipe_gap = random.randint (150, 260)
pipe_speed = 6
fps = 60
pipe_distance = 480

#movimiento
fondo_x = 0
fondo_vel = 1.5

current_distance = 0
average_distance = 0
best_distance=0
scroll_speed = 1
speed = scroll_speed
generacion=1
max_generaciones = 100  #tope de geenraciones, si pasa esto se termina el juego

class Tubo:

    def __init__(self, posicion_x, imagen_arriba, imagen_abajo):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed
        self.gap = random.randint(190,220)

        self.imagen_arriba_original = imagen_arriba
        self.imagen_abajo_original = imagen_abajo
        # altura de tubos
        self.altura_superior = random.randint(110, height - self.gap - 110)
        self.altura_inferior = self.altura_superior + self.gap
        # rectángulos
        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior)
        self.rect_abajo = pygame.Rect(
            self.x, self.altura_inferior, self.ancho, height - self.altura_inferior
        )

    def mover(self):
        """Mueve el tubo para la izquierda"""
        self.x -= self.velocidad
        self.rect_arriba.x = int(self.x)
        self.rect_abajo.x = int(self.x)

    def dibujar(self, pantalla):
        """Dibujo los tubos con sus imágenes"""
        # tubo de arriba
        imagen_arriba = pygame.transform.scale(
            self.imagen_arriba_original, (self.ancho, self.altura_superior)
        )
        pantalla.blit(imagen_arriba, (self.x, 0))

        # tubo de abajo
        altura_abajo = height - self.altura_inferior
        imagen_abajo = pygame.transform.scale(
            self.imagen_abajo_original, (self.ancho, altura_abajo)
        )
        pantalla.blit(imagen_abajo, (self.x, self.altura_inferior))

        # para debug:
        # pygame.draw.rect(pantalla, (0, 255, 0), self.rect_arriba, 2)
        # pygame.draw.rect(pantalla, (0, 255, 0), self.rect_abajo, 2)

    def nuevos_tubos(self):
        """Elimina tubos viejos y crea nuevos a la derecha"""
        return self.x + self.ancho < 2

    def centro_del_hueco(self):
        """Devuelve la posición y del centro del hueco"""
        return self.altura_superior + self.gap / 2


#empieza el juego

pygame.init()
clock = pygame.time.Clock()
pygame.mixer.music.load("fondo_musica.mp3")
pygame.mixer.music.play(-3) 
sonido_next_gen = pygame.mixer.Sound("next_round.mp3")

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Angry Flappy Bird")

icon = pygame.image.load("Imágenes/pajaro_icono.png")
pygame.display.set_icon(icon)

perdio = pygame.image.load("Imágenes/game_over.png")
game_over = False

fondo = pygame.image.load("Imágenes/fondo.png")

#jugador
playerImg = pygame.image.load("Imágenes/pajaro.png")
playerX = 120
playerY = 420

vel_y = 0
gravedad = 0.5

#tubos
tubo_arriba = pygame.image.load("Imágenes/tubo arriba.png")
tubo_abajo = pygame.image.load("Imágenes/TUBO ABAJO.png")


#primeros tres tubos
tubos = [Tubo(300, tubo_arriba, tubo_abajo),Tubo(300 + pipe_distance, tubo_arriba, tubo_abajo),Tubo(300 + 2 * pipe_distance, tubo_arriba, tubo_abajo),]

#poblacion inicial
poblacion = Poblacion(None)

#loop
tiempo_vivo = 0
max_tiempo_vivo = 0
longest_survival=0
survivors_120s= 0

running = True
pajaros_tiempo_max = 0
tiempo_limite = 20 * 60 #límite de 120 segundos, termina el juego
fin_por_tiempo = False
while running:
    

    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if fin_por_tiempo==True:
            running=False
        #if event.type == pygame.KEYDOWN:
         #   if event.key == pygame.K_1:
          #      scroll_speed = 1
   #        # if event.key == pygame.K_2:
    #            scroll_speed = 2
     #       if event.key == pygame.K_3:
      #          scroll_speed = 3
       #     if event.key == pygame.K_4:
        #        scroll_speed = 4
         #   if event.key == pygame.K_5:
          #      scroll_speed = 5

            # actualizar velocidad de tubos
            for tubo in tubos:
                tubo.velocidad = scroll_speed

    #fondo se mueve
    fondo_x -= fondo_vel
    if fondo_x <= -width:
        fondo_x = 0
    screen.blit(fondo, (fondo_x, 0))
    screen.blit(fondo, (fondo_x + width, 0))

    #pajaros 
    vivos = 0  #contador de pájaros vivos

    for pajaro in poblacion.pobl:
        if not pajaro.vida:
            continue  #ignoramos los muertos

        vivos += 1

        #el pajaro apunta al tubo
        prox_tubo = tubos[0]
        coordt = (prox_tubo.x, prox_tubo.centro_del_hueco())

        #aleteo
        pajaro.aletear(coordt)

        #actualiza física
        pajaro.actualizar()

        #if pajaro.vida and pajaro.rendimiento >= tiempo_limite:
        #    if not pajaro.contado_para_max:
        #        pajaros_tiempo_max += 1
            # opcional: marcarlo como ya contado para que no sume varias veces
        #        pajaro.contado_para_max = True

        if not paso_tubo(pajaro, tubos, playerImg):
            pajaro.vida= False
      
        #si sigue vivo lo dibujo
        if pajaro.vida:
            screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))

    if pajaros_tiempo_max >= 30:
        running = False

    if vivos > 0:
        tiempo_vivo += 1

    #tubos
    for tubo in list(tubos):
        tubo.mover()
        tubo.dibujar(screen)

    #reemplazo los tubos 
    if tubos[0].nuevos_tubos():
        tubos.pop(0)
        nueva_x = tubos[-1].x + pipe_distance
        tubos.append(Tubo(nueva_x, tubo_arriba, tubo_abajo))

    poblacion_viva = [p for p in poblacion.pobl if p.vida]

    if tiempo_vivo==tiempo_limite:
        if len(poblacion_viva)>= 1: ####
            fin_por_tiempo= True
        else:
            survivors_120s= len(poblacion_viva)

    if vivos== 0:
        # Reproducir voz "Next Generation"
        sonido_next_gen.play()


        # Esperar a que termine (1.5 segundos)
        #pygame.time.delay(1500)


        mejores = poblacion.seleccion()
        nueva_gen= poblacion.cruzar(mejores)
        poblacion.pobl= nueva_gen
        poblacion.mutar()

        generacion+=1
        if generacion > max_generaciones:
            running = False
        if tiempo_vivo>max_tiempo_vivo:
            max_tiempo_vivo= tiempo_vivo
        if current_distance> best_distance:
            best_distance=current_distance
        #resteamos estadisticas para la nueva generacion
        current_distance=0
        tiempo_vivo=0
        tubos= [Tubo(600, tubo_arriba, tubo_abajo), Tubo(600 + pipe_distance, tubo_arriba, tubo_abajo), Tubo(600 + 2 * pipe_distance, tubo_arriba, tubo_abajo),]

    #estadisiticas
    panel_width = 250
    panel_x = width - panel_width
    pygame.draw.rect(screen, (0, 0, 0), (panel_x, 0, panel_width, height))

    font_titulo = pygame.font.SysFont("Century Gothic", 24, bold=False)
    titulo = font_titulo.render("GA Statistics", True, (250, 250, 250))
    screen.blit(titulo, (panel_x + 20, 10))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render(f"Generation: {generacion}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 60))

    texto = font.render(f"Alives: {vivos}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 80))

    texto = font.render("Prev Gen 2min: ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 100))

    texto = font.render(f"Speed: {scroll_speed}X ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 120))

    current_distance += 1
    texto = font.render(f"Current Distance: {current_distance}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 160))

    #Mejor Distancia
    mejor_distancia = max(p.rendimiento for p in poblacion.pobl)
    texto = font.render(f"Best Distance: {best_distance} ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 180))

    texto = font.render(f"Current Survival: {tiempo_vivo / fps:.2f}s", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 220))

    texto = font.render(f"Best time: {max_tiempo_vivo/ fps:.2f}s", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 240))

    texto = font.render(f"120s Survivors: {survivors_120s}", True, (250,250,250))
    #texto = font.render(f"Last Gen Survival: {max_tiempo_vivo / fps:.2f}s", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 260))

    #Diatncia promedio
    distancia = [p.rendimiento for p in poblacion.pobl]
    if len(distancia) > 0:
        promedio = sum(distancia) / len(distancia)
    else:
        promedio = 0
        
    texto = font.render("Avg Distance: ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 200))
    clock.tick(fps)

    dibujar_genoma(screen, poblacion_viva, panel_x+20, 300)

    pygame.display.update()

pygame.quit()















