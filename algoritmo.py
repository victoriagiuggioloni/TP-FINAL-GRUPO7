import random
import pygame


height = 600
width = 1000
gravedad = 0.5
flap_strength = -10
pipe_width = 70
pipe_gap = 200
pipe_speed = 6

class Tubo:
    def __init__(self, posicion_x):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed

        self.altura_superior = random.randint(50, height - pipe_gap - 50)
        self.altura_inferior = self.altura_superior + pipe_gap

        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior)




pobl=[]
for pajaro in range(99):
    w=[]
    for peso in range(6):
        w.append(round(random.uniform(-1, 1), 2))
    pobl.append(w)
print(w)
print(pobl)




class pajaro:
    def __init__(self, w, vy):
        self.w0= w[0]
        self.w1= w[1]
        self.w2= w[2]
        self.w3= w[3]
        self.w4= w[4]
        self.w5= w[5]
        self.vy= vy

    

