
import random
import pygame
from funciones import *


height = 600
width = 1000
gravedad = 0.5
flap_strength = -8
pipe_width = 70
pipe_gap = 200
pipe_speed = 6

class Pajaro:
    def __init__(self, w):
        if w==None:
            w=[]
            for peso in range(6):
                w.append(round(random.uniform(-5, 5), 2))
        self.w= w
        self.vy= 0
        self.y= 420
        self.coordp= [120, self.y]
        self.volar= False
        self.rendimiento= 0
        self.vida= True
        self.altura = 34 

    def aletear(self, coordt): # coord= (x, y) #coordp ya la tengo seria self.coordp
      Dx= abs(self.coordp[0]- coordt[0])
      Dy= abs(self.coordp[1]- coordt[1])
      self.volar= self.w[0]+self.w[1]*Dy + self.w[2]*(Dy**2) + self.w[3]*Dx + self.w[4]*(Dx**2) + self.w[5]*self.vy >0
      if self.volar is True:
        self.vy = flap_strength

    def actualizar(self):
      if not self.vida:
          return
      
      self.vy += gravedad
      self.y+= self.vy
      self.coordp[1]= self.y

      if self.y < 0 or self.y > height - self.altura:
         self.vida = False
      else:
         self.rendimiento += 1  #fitness,
      #sumamos distancia recorrdia frame a frame


class Poblacion:
    def __init__(self, pobl):
        if pobl == None:
            pobl=[]
            for p in range(100):
                pobl.append(Pajaro(None)) 

        self.pobl= pobl

    def seleccion(self):
      mejores = sorted(self.pobl, key=lambda p: p.rendimiento, reverse=True)[ :30]
      return mejores

    def cruzar(self, mejores):
      nueva_gen=[]
      for nuevo_p in range(100):
        w_hijo=[]
        padre, madre= random.choices(mejores, k=2)
        for gen in range(6):
          if random.random()<0.5:
             w_hijo.append(padre.w[gen])
          else:
             w_hijo.append(madre.w[gen])
        
        hijo= Pajaro(w_hijo)

        hijo.rendimiento = 0
        hijo.vida = True
        hijo.vy = 0
        hijo.y = 420
        hijo.coordp = [120, hijo.y]
        nueva_gen.append(hijo)
      
      return nueva_gen

    def mutar(self):
      for p in self.pobl:
        for i in range(6):
          if random.random() < 0.2:
              p.w[i]+=round(random.uniform(-0.2, 0.2), 2)  # mutación
              p.w[i] = max(-2, min(1, p.w[i]))
