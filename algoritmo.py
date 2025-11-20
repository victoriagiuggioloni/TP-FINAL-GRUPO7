
import random
import pygame


height = 600
width = 1000
gravedad = 0.5
flap_strength = -10
pipe_width = 70
pipe_gap = 200
pipe_speed = 6

class Pajaro:
    def __init__(self, w):
        if w==None:
            w=[]
            for peso in range(6):
                w.append(round(random.uniform(-1, 1), 2))
        self.w= w
        self.vy= 0
        self.y= 420
        self.coordp= [120, self.y]
        self.volar= False
        self.rendimiento= 0
        self.vida= True

    def aletear(self, coordt): # coord= (x, y) #coordp ya la tengo seria self.coordp
      Dx= abs(self.coordp[0]- coordt[0])
      Dy= abs(self.coordp[1]- coordt[1])
      self.volar= self.w[0]+self.w[1]*Dy + self.w[2]*(Dy**2) + self.w[3]*Dx + self.w[4]*(Dx**2) + self.w[5]*self.vy >0
      if self.volar is True:
        self.vy+= flap_strength

    def actualizar(self):
      if not self.vida:
          return
      
      self.vy += gravedad
      self.y+= self.vy
      self.coordp[1]= self.y

         
      if self.y < 0 or self.y > height:
         self.vida = False

        
         self.rendimiento += 1  #fitness


class Poblacion:
    def __init__(self, pobl):
        if pobl == None:
            pobl=[]
            for p in range(100):
                pobl.append(Pajaro(None))
                #print(w)
                #print(pobl)
        self.pobl= pobl
        
    def ver_rendimiento(self, ):
            #ver como hacer el codigo para que vuele
            #devuelve una lista con los rendimientos de cada pajaro

    #def seleccion(self, ):
        pass
        #ordenar de mayor a menor y quedarme con los 50 mejores, devuelve self.mejores

    #def cruzar(self, ):
            #cruzar pajaros(self.mejores) para conseguir la nueva pobl
        