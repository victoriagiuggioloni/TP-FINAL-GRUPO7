import pygame
import random
from algoritmo import Poblacion

height = 600
width = 1000
pipe_width = 80
pipe_gap = 200
pipe_speed = 6
fps = 60
pipe_distance = 480

#movimiento
fondo_x = 0
fondo_vel = 1.5

current_distance = 0
average_distance = 0
scroll_speed = 3
speed = scroll_speed


class Tubo:

    def __init__(self, posicion_x, imagen_arriba, imagen_abajo):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed

        self.imagen_arriba_original = imagen_arriba
        self.imagen_abajo_original = imagen_abajo
        # altura de tubos
        self.altura_superior = random.randint(110, height - pipe_gap - 110)
        self.altura_inferior = self.altura_superior + pipe_gap
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
        return self.altura_superior + pipe_gap / 2


#empieza el juego

pygame.init()
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

clock = pygame.time.Clock()

#primeros tres tubos
tubos = [Tubo(600, tubo_arriba, tubo_abajo),Tubo(600 + pipe_distance, tubo_arriba, tubo_abajo),Tubo(600 + 2 * pipe_distance, tubo_arriba, tubo_abajo),]

#poblacion inicial
poblacion = Poblacion(None)

#loop

running = True
while running:
    clock.tick(fps)

    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

        #no toca el techo
        if pajaro.y < 0:
            pajaro.y = 0
            pajaro.vy = 0
            pajaro.coordp[1] = pajaro.y

        #no toca el piso
        if pajaro.y > height - playerImg.get_height():
            pajaro.y = height - playerImg.get_height()
            pajaro.vy = 0
            pajaro.coordp[1] = pajaro.y

        # hitbox
        player_hit = pygame.Rect(pajaro.coordp[0],pajaro.coordp[1],playerImg.get_width(),playerImg.get_height(),)

        #mueren si tocan los tubos
        for tubo in tubos:
            if player_hit.colliderect(tubo.rect_arriba) or player_hit.colliderect(tubo.rect_abajo):
                pajaro.vida = False
                break

        #si sigue vivo lo dibujo
        if pajaro.vida:
            screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))

    #tubos
    for tubo in list(tubos):
        tubo.mover()
        tubo.dibujar(screen)

    #reemplazo los tubos 
    if tubos[0].nuevos_tubos():
        tubos.pop(0)
        nueva_x = tubos[-1].x + pipe_distance
        tubos.append(Tubo(nueva_x, tubo_arriba, tubo_abajo))

    #estadisiticas
    panel_width = 250
    panel_x = width - panel_width
    pygame.draw.rect(screen, (0, 0, 0), (panel_x, 0, panel_width, height))

    font_titulo = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
    titulo = font_titulo.render("GA Statistics", True, (250, 250, 250))
    screen.blit(titulo, (panel_x + 20, 10))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render("Generation: ", True, (250, 250, 250))
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
    texto = font.render(f"Best Distance: {mejor_distancia} ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 180))

    #Diatncia promedio
    distancia = [p.rendimiento for p in poblacion.pobl]
    if len(distancia) > 0:
        promedio = sum(distancia) / len(distancia)
    else:
        promedio = 0
        
    texto = font.render("Avg Distance: ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 200))

    pygame.display.update()

pygame.quit()















