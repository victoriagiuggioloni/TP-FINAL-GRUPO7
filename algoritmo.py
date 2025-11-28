
import random
import pygame
from funciones import *



height = 600
width = 1000
gravedad = 0.5
flap_strength = -10
pipe_width = 70
pipe_gap = 200
pipe_speed = 8

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
      #VICKY
      #d_x = tubo.x - self.coordp[0]
      #d_up = self.coordp[1] - tubo.altura_superior
      #d_down = tubo.altura_inferior - (self.coordp[1] + self.altura)

     # ACTUALIZE ACA - VICKY
      #n_dx = d_x / width
      #n_up = d_up / height
      #n_down = d_down / height
      #n_vy = self.vy / 10
      #self.volar = (self.w[0]+ self.w[1]*n_up+ self.w[2]*n_down+ self.w[3]*n_dx+ self.w[4]*n_vy) > 0
      self.volar= self.w[0]+self.w[1]*Dy + self.w[2]*(Dy**2) + self.w[3]*Dx + self.w[4]*(Dx**2) + self.w[5]*self.vy >0
      if self.volar and self.vy >= 0: #solo aletea si esta cayendo
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
         self.rendimiento += 1  #fitness, sumamos distancia recorrdia frame a frame
         if self.rendimiento > 120 * 60: #límite de 120 segundos, cuando un pájaro supera esto, termina el juego
           self.vida = False


class Poblacion:
    def __init__(self, pobl):
        if pobl == None: 
            pobl=[]
            for p in range(100): #bucle para crear 100 pájaros
                pobl.append(Pajaro(None)) #cada pájaro se crea sin pesos

        self.pobl= pobl

    def seleccion(self):
      mejores = sorted(self.pobl, key=lambda p: p.rendimiento, reverse=True)[ :15] #ordena la pob de menor a mayor, toma los 15 mejores según su rendimiento
      return mejores 

    def cruzar(self, mejores): #crea nueva generación mezclando los pesos de los mejores pájaros (mejores es la lista de los 15 padres)
      nueva_gen=[] #lista vacía donde se almacenarán los hijos
      for nuevo_p in range(100): #bucle crea 100 pájaros nuevos
        w_hijo=[] #lista vacía con pesos del hijo
        padre, madre= random.choices(mejores, k=2)   #elige aleatoriamente dos padres de la lista de los mejores
        for gen in range(6):  #recorre los 6 pesos del pajaro
          if random.random()<0.5:
             w_hijo.append(padre.w[gen]) #cruza genes de los 2 pájaros con 50% de prob
          else:
             w_hijo.append(madre.w[gen]) #cruza genes
        
        hijo= Pajaro(w_hijo) #crea hijo en base a la mezcla de genes

        hijo.rendimiento = 0
        hijo.vida = True
        hijo.vy = 0
        hijo.y = 420
        hijo.coordp = [120, hijo.y]
        nueva_gen.append(hijo) #va agregando los hijos a la lista de los 100 nuevos
      
      return nueva_gen #devuelve lista completa de nuevos 100 pajaros

    def mutar(self): #aplica mutaciones aleatorias a la población
      for p in self.pobl: #para cada pájaro p en pobl
        for i in range(6): #recorre sus 6 pesos/genes
          if random.random() < 0.2: #cambia el peso con la prob del 20%
              p.w[i]+=round(random.uniform(-0.2, 0.2), 2)  # mutación, añade pequeño valor aleatorio
              p.w[i] = max(-2, min(1, p.w[i])) #asegura que el peso se mantenga dentro de un rango de -2 a 1
