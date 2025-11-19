
import random
import pygame


height = 600
width = 1000
gravedad = 0.5
flap_strength = -10
pipe_width = 70
pipe_gap = 200
pipe_speed = 6



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
    


