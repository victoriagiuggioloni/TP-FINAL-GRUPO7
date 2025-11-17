
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

        self.altura_superior = random.randint(50, height - pipe_gap - 50) #altura del tubo de arriba
        self.altura_inferior = self.altura_superior + pipe_gap #donde empieza el tubo de abajo

        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior) #calculo el rectangulo de arriba
        self.rect_abajo = pygame.Rect(self.x, self.altura_inferior, self.ancho, height - self.altura_inferior) 

    def mover(self):
        """Mueve el tubo para la izquierda"""
        self.x -= self.velocidad #más avanza a la derecha, más a la izquierda se mueve el tubo
        self.rect_arriba.x = int(self.x)
        self.rect_abajo.x = int(self.x)

    def dibujar(self, pantalla):
        """Dibujo los tubos con RGB"""
        pygame.draw.rect(pantalla, (0, 255, 0), self.rect_arriba)
        pygame.draw.rect(pantalla, (0, 255, 0), self.rect_abajo)

    def nuevos_tubos(self):
        """Elimina tubos viejos y crea nuevos a la derecha"""
        return self.x + self.ancho < 0
    
    def centro_del_hueco(self):
        """Devuelve la posición y del centro del hueco para que el pájaro sepa dónde apuntar"""
        return self.altura_superior + pipe_gap / 2

class Poblacion:
    def __init__(self, pobl):
        if pobl == None:
            pobl=[]
            for p in range(99):
                pobl.append(Pajaro(None, 0))
                #print(w)
                #print(pobl)
        self.pobl= pobl
        
    def ver_rendimiento(self, ):
            #ver como hacer el codigo para que vuele
            #devuelve una lista con los rendimientos de cada pajaro
    def seleccion(self, ):
        #ordenar de mayor a menor y quedarme con los 50 mejores, devuelve self.mejores

    def cruzar(self, ):
            #cruzar pajaros(self.mejores) para conseguir la nueva pobl
        
class Pajaro:
    def __init__(self, w, vy, posicion): #tb deberia recibir la posicion del pajaro
        if w==None:
            w=[]
            for peso in range(6):
                w.append(round(random.uniform(-1, 1), 2))
        self.w= w
        self.vy= vy
        self.coordp= posicion

    def aletear(self, coordp, coordt): # coord= (x, y) #coordp ya la tengo seria self.coordp
        Dx= abs(coordp[0]- coordt[0])
        Dy= abs(coordp[1]- coordt[1])
        volar= self.w[0]+self.w[1]*Dy + self.w[2]*(Dy**2) + self.w[3]*Dx + self.w[4]*(Dx**2) + self.w[5]*self.vy
        return volar
    


