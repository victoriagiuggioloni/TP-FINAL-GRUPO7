import random
import pygame

#Variables fijas:
height = 600
width = 1000
gravedad = 0.5
flap_strength = -7
pipe_width = 80
pipe_gap = random.randint (150, 260)
fps = 60
pipe_distance = 480

pipe_speed = 8

#Funciones adicionales:
def pajaro_muerto_imagen(image: pygame.Surface) -> pygame.Surface:
    '''
    Convierte una imagen de Pygame a blanco y negro.
    Reduce su opacidad para simular visualmente que el pájaro está muerto.
    Devuelve una nueva superficie con la nueva imagen en escala de grises y mayor transparencia.
    '''

    # ancho (w) y el alto (h) de la imagen original
    w, h = image.get_size()
    #Creamos una nueva superficie vacía del mismo tamaño,
    #con alpha (transparencia)
    gris = pygame.Surface((w, h), pygame.SRCALPHA)
    #Recorremos pixel por pixel
    for x in range(w):
        for y in range(h):
            #color del pixel actual (r, g, b, a)
            r, g, b, a = image.get_at((x, y))
            #Calculamos el valor del pixel de color a escala de grises
            #(rojo + verde + azul) // 3
            v = (r + g + b) // 3
            #Convertimos la imagen a la escala de grises y mantenemos transparencia
            nuevo_alpha = int(a * 0.4)   #más transparente
            gris.set_at((x, y), (v, v, v, nuevo_alpha))

    #imagen con escala de grises
    return gris

def paso_tubo(pajaro:list, tubos:list, playerImg:pygame.Surface) -> bool:
    '''
    Comprueba si el pájaro choca con alguno de los tubos de la pantalla.


    Crea un área de colisión (hitbox) ligeramente reducida alrededor del pájaro
    para evitar falsos positivos y la compara con los rectángulos de los tubos
    superiores e inferiores.


    Devuelve: `True` si el pájaro no colisiona con ningún tubo, `False` si se detecta una colisión con el tubo.


    '''
    
    #player_hit = pygame.Rect(pajaro.coordp[0],pajaro.coordp[1],playerImg.get_width(),playerImg.get_height(),)
    player_hit = pygame.Rect(pajaro.coordp[0]+5, pajaro.coordp[1]+5, 
                         playerImg.get_width()-10, playerImg.get_height()-10) #reduce falsos positivos
    #si el hitbox del pájaro toca el hitbox de los tubos, muere el pájaro
    for tubo in tubos:
        if player_hit.colliderect(tubo.rect_arriba) or player_hit.colliderect(tubo.rect_abajo): #devuelve True si los rectangulos se superponen
            return False #como es True que se superponen rectángulos, devuelve Falseporque el pájaro NO pasó
    return True #si terminó el fro y no detectó colisiones/superposiciones devuelve True (el pájaro sí pasó)

def dibujar_genoma(screen: pygame.Surface, poblacion: list, x: int, y: int) -> None:
    """
    Dibuja en la pantalla barras horizontales que representan el valor promedio de cada peso W0 a W5 de la población actual de pájaros.
    Utiliza colores verde para promedios positivos y rojo para negativos y muestra el valor numérico promedio al lado de cada barra.

    """
    fuente = pygame.font.SysFont("arial", 16) #crea fuente para escribir 
    ancho_max = 70 #largo horizontal máx de las barras
    espacio = 25 #espacio entre barras

    lista_w = list(zip(*[p.w for p in poblacion])) #toma los valores w de cada pájaro y los reorganiza para poder calcular promedio de c/uno

    for i, pesos in enumerate(lista_w): #recorre cada lista de pesos (índice y valor)

        prom = sum(pesos) / len(pesos) #promedio de peso

        barra = int((prom / 5) * ancho_max) #convierte prom en el largo horizontal de la barra
        #divide por 5 porque los pesos van entre -5 y 5
        by = y + i * espacio #posición vertical donde se dibbujará la barra

        txt = fuente.render(f"w{i}:", True, (255, 255, 255))
        screen.blit(txt, (x, by))
        #dibuja dos líneas grises 
        pygame.draw.line(screen, (80, 80, 80), (x + 100, by + 10), (x + 100 + ancho_max, by + 10), 2)
        pygame.draw.line(screen, (80, 80, 80), (x + 100, by + 10), (x + 100 - ancho_max, by + 10), 2)

        color = (0, 200, 0) if prom > 0 else (200, 50, 50) #prom + barra verde, prom - barra roja

        if barra >= 0: 
            pygame.draw.rect(screen, color, (x + 100, by + 5, barra, 10)) #dibuja la barra hacia la der si el prom es positivo
        else:
            pygame.draw.rect(screen, color, (x + 100 + barra, by + 5, -barra, 10)) #a la izq si el prom es negativo

        val = fuente.render(f"{prom:.2f}", True, (255, 255, 255))
        screen.blit(val, (x + 180, by)) #escribe num del promedio a la derecha


#Clases:
class Pajaro:
    def __init__(self, w): #crea un pájaro con genes aleatorios, listo para volar y medir su desempeño
        if w==None: #w:lista de los 6 pesos/genes
            w=[] 
            for peso in range(6): 
                w.append(round(random.uniform(-5, 5), 2)) #si no se pasa genes, se generan aleatorios
        self.w= w
        self.flap_strength= flap_strength #
        self.vy= 0 #velocidad vertical empieza en cero
        self.y= 420
        self.coordp= [120, self.y]
        self.volar= False #indica si aletea 
        self.rendimiento= 0 #cuantos frames sobrevivio
        self.vida= True #indica si esta vivo
        self.altura = 34 #tamaño del pájaro para colisiones
        self.dead = False                                        ############
        self.dead_image = None

    def aletear(self, coordt: tuple) -> None: 
      '''
      Decide si el pájaro debe aletear basándose en sus pesos y la posición del próximo tubo.
      '''
     #coordp: self.coordp #coordt: posición del prox tubo(x, y del centro del hueco)
      Dx= abs(self.coordp[0]- coordt[0]) #distancia horizontal al tubo
      Dy= abs(self.coordp[1]- coordt[1]) #distancia vertical al hueco
     
      #decide si aletear según los genes y las siguientes distancias:
      self.volar= self.w[0]+self.w[1]*Dy + self.w[2]*(Dy**2) + self.w[3]*Dx + self.w[4]*(Dx**2) + self.w[5]*self.vy >0
      if self.volar and self.vy >= 0: #solo aletea si volar = True o si está cayendo
        #self.vy = flap_strength #usando sus genes y la posición del tubo, decide si aletear hacia arriba
        self.vy = self.flap_strength

    def actualizar(self) -> None: 
      '''
      Aplica gravedad, mueve al pájaro, comprueba los límites de la pantalla y actualiza su rendimiento.
      '''
      
      if not self.vida: #si el pájaro murió, la función no ejecuta nada más (evita que pájaros muertos sigan cambiando la posición)
          return
      
      self.flap_strength= flap_strength
      self.vy += gravedad #aplica gravedad a la velocidad vertical
      self.y+= self.vy #actualiza la posicion vertical sumandole la velocidad vertical
      self.coordp[1]= self.y

      if self.y <= 0 or self.y >= height - self.altura -30:
         self.morir() #comprueba si se salió de la pantalla
         self.vida = False #si sí entonces muere
         self.dead_image = pajaro_muerto_imagen(playerImg)
      else:
         self.rendimiento += 1  #si no muere, fitness, sumamos distancia recorrdia frame a frame 

    def morir(self) -> None:      
        '''
        Marca el pájaro como muerto, detiene su actualización y cambia su imagen por una versión en escala de grises.
        '''                          
        if self.dead:
            return #ya procesado
        self.vida = False
        self.dead = True
        #Convertimos a gris:
       # self.dead_image = pajaro_muerto_imagen(playerImg)


class Poblacion:
    def __init__(self, pobl):
        if pobl == None: 
            pobl=[]
            for p in range(100): #bucle para crear 100 pájaros
                pobl.append(Pajaro(None)) #cada pájaro se crea sin pesos

        self.pobl= pobl

    def seleccion(self) -> list:
      """
      Selecciona y devuelve los 30 mejores pájaros de la población actual basado en su rendimiento .
      """
      mejores = sorted(self.pobl, key=lambda p: p.rendimiento, reverse=True)[ :30] #ordena la pob de menor a mayor, toma los 30 mejores según su rendimiento
      return mejores 

    def cruzar(self, mejores: list) ->list: 
      """
      Crea una nueva generación de 100 pájaros mediante cruce de los 30 pájaros seleccionados, usando selección por rango.
      """
      #crea nueva generación mezclando los pesos de los mejores pájaros (mejores es la lista de los 15 padres)
      nueva_gen=[] #lista vacía donde se almacenarán los hijos
      num_padres = len(mejores) # 30 padres
      pesos = list(range(num_padres, 0, -1)) #mayor probabilidad de que salga el mejor
      for _ in range(100):
        w_hijo = []
        padre, madre = random.choices(mejores, weights=pesos, k=2)  #elige aleatoriamente dos padres de la lista de los mejores
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

    def mutar(self) -> None:
      '''
      Aplica mutaciones aleatorias a la población
      '''
        #aplica mutaciones aleatorias a la población
      for p in self.pobl: #para cada pájaro p en pobl
        for i in range(6): #recorre sus 6 pesos/genes
          if random.random() < 0.2: #cambia el peso con la prob del 20%
              p.w[i]+=round(random.uniform(-0.1, 0.1), 2)  # mutación, añade pequeño valor aleatorio
              p.w[i] = max(-2, min(1, p.w[i])) #asegura que el peso se mantenga dentro de un rango de -2 a 1

class Tubo:

    def __init__(self, posicion_x, imagen_arriba, imagen_abajo):
        self.x = posicion_x
        self.ancho = pipe_width
        self.velocidad = pipe_speed
        self.gap = random.randint(190,220) #el hueco de los tubos es aleatorio

        self.imagen_arriba_original = imagen_arriba
        self.imagen_abajo_original = imagen_abajo
        # altura de tubos
        self.altura_superior = random.randint(110, height - self.gap - 110)
        self.altura_inferior = self.altura_superior + self.gap
        # rectángulos(hitbox)
        self.rect_arriba = pygame.Rect(self.x, 0, self.ancho, self.altura_superior)
        self.rect_abajo = pygame.Rect(self.x, self.altura_inferior, self.ancho, height - self.altura_inferior )

    def mover(self):
        """Mueve el tubo para la izquierda"""
        self.x -= self.velocidad
        self.rect_arriba.x = int(self.x)
        self.rect_abajo.x = int(self.x)

    def dibujar(self, pantalla):
        """Dibujo los tubos con sus imágenes"""
        # tubo de arriba
        imagen_arriba = pygame.transform.scale(self.imagen_arriba_original, (self.ancho, self.altura_superior))
        pantalla.blit(imagen_arriba, (self.x, 0))

        # tubo de abajo
        altura_abajo = height - self.altura_inferior
        imagen_abajo = pygame.transform.scale(self.imagen_abajo_original, (self.ancho, altura_abajo) )
        pantalla.blit(imagen_abajo, (self.x, self.altura_inferior))

    def nuevos_tubos(self):
        """Elimina tubos viejos y crea nuevos a la derecha"""
        return self.x + self.ancho < 2

    def centro_del_hueco(self):
        """Devuelve la posición y del centro del hueco"""
        return self.altura_superior + self.gap / 2


#Inicialización Python:
pygame.init()
clock = pygame.time.Clock()

#Sonido:
pygame.mixer.music.load("Auxiliar/Musica/fondo_musica.mp3")
pygame.mixer.music.play(-3) 
sonido_next_gen = pygame.mixer.Sound("Auxiliar/Musica/next_round.mp3")

#Pantalla de juego:
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Angry Flappy Bird")
icon = pygame.image.load("Auxiliar/Imágenes/pajaro_icono.png")
pygame.display.set_icon(icon)
perdio = pygame.image.load("Auxiliar/Imágenes/game_over.png")
game_over = False
fondo = pygame.image.load("Auxiliar/Imágenes/fondo.png")

#Jugador:
playerImg = pygame.image.load("Auxiliar/Imágenes/pajaro.png")
playerX = 120
playerY = 420

#Variables del fondo:
fondo_x = 0
fondo_vel = 1.5

#Tubos iniciales:
tubo_arriba = pygame.image.load("Auxiliar/Imágenes/tubo arriba.png")
tubo_abajo = pygame.image.load("Auxiliar/Imágenes/TUBO ABAJO.png")
#Primeros tres tubos
tubos = [Tubo(300, tubo_arriba, tubo_abajo),Tubo(300 + pipe_distance, tubo_arriba, tubo_abajo),Tubo(300 + 2 * pipe_distance, tubo_arriba, tubo_abajo),]

#Poblacion inicial:
poblacion = Poblacion(None)

#Variables del loop:
running = True
scroll_speed = 1
speed = scroll_speed
max_generaciones = 100
tiempo_limite = 120 * 60 #límite de 120 segundos, termina el juego
fin_por_tiempo = False
vel_y = 0
velocidad_maxima= 12


#Variables de las estadísticas:
tiempo_vivo = 0
max_tiempo_vivo = 0 
survivors_120s= 0
current_distance = 0
average_distance = 0
best_distance=0
generacion=1
promedio = 0

while running:
    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Aumentas la variable pipe_speed
                fps+=15
                pipe_speed += 2
                flap_strength-=1
                gravedad+= 0.5
                speed+=1
                
                # Controlas el límite: si se pasa de 8, vuelve a 6
                if pipe_speed > velocidad_maxima:
                    fps= 60
                    pipe_speed = 6
                    flap_strength=-7
                    gravedad = 0.5
                    speed=1

    #fondo se mueve
    fondo_x -= fondo_vel
    if fondo_x <= -width:
        fondo_x = 0
    screen.blit(fondo, (fondo_x, 0))
    screen.blit(fondo, (fondo_x + width, 0))

    #pajaros 
    #vivos = 0  #Contador de pájaros vivos
    for pajaro in poblacion.pobl:
        if not pajaro.vida: #dibujamos los muertos
            if pajaro.dead_image is None:
                pajaro.dead_image = pajaro_muerto_imagen(playerImg)
            screen.blit(pajaro.dead_image, (pajaro.coordp[0], pajaro.coordp[1]))

    for pajaro in poblacion.pobl:
        # Si está vivo, actualizamos física y decisión
        if pajaro.vida:
            #vivos += 1

            #El pajaro apunta al tubo:
            prox_tubo = tubos[0]
            coordt = (prox_tubo.x, prox_tubo.centro_del_hueco())

            #Actualiza física:
            pajaro.actualizar()

            #Aletear:
            pajaro.aletear(coordt)

            # Colisión:
            if not paso_tubo(pajaro, tubos, playerImg):
                pajaro.morir()

            #Dibujo pajaro vivo a color:
            screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))

        # Dibujado: si está vivo dibujo color, si murió dibujo gris (quieto)
 #       if pajaro.vida:
  #          screen.blit(playerImg, (pajaro.coordp[0], pajaro.coordp[1]))
   #     elif pajaro.dead:
    #        # asegurate que dead_image exista (se crea en morir)
     #       if pajaro.dead_image is None:
      #          pajaro.dead_image = pajaro_muerto_imagen(playerImg)
       #     screen.blit(pajaro.dead_image, (pajaro.coordp[0], pajaro.coordp[1]))

        #if pajaro.vida: #dibujamos los vivos en un bucle aparte para que se dibujen por encima de los muertos
            # asegurate que dead_image exista (se crea en morir)
            
            
 
    poblacion_viva = [p for p in poblacion.pobl if p.vida]
    vivos= len(poblacion_viva)

    if tiempo_vivo==tiempo_limite:
        if vivos>= 30: ####
            fin_por_tiempo= True
            print('hola')
        else:
            if vivos> survivors_120s:
                survivors_120s= len(poblacion_viva)

    if vivos > 0:
        tiempo_vivo += 1
    
    #Tubos:
    for tubo in list(tubos):
        tubo.velocidad= pipe_speed
        tubo.mover()
        tubo.dibujar(screen)

    #Reemplazo los tubos:
    if tubos[0].nuevos_tubos():
        tubos.pop(0)
        nueva_x = tubos[-1].x + pipe_distance
        tubos.append(Tubo(nueva_x, tubo_arriba, tubo_abajo))

    if fin_por_tiempo==True:
            running=False

    if vivos== 0: 
        sonido_next_gen.play() #Reproducir voz "Next Generation"

        #Distancia promedio:
        distancia = [p.rendimiento for p in poblacion.pobl]
        if len(distancia) > 0:
            promedio = sum(distancia) / len(distancia)
        else:
            promedio = 0

        #Creamos una nueva generación:
        mejores = poblacion.seleccion()
        nueva_gen= poblacion.cruzar(mejores)
        poblacion.pobl= nueva_gen
        poblacion.mutar()

        #Actualizamos estadística del panel:
        generacion+=1
        if generacion > max_generaciones:
            running = False
        if tiempo_vivo>max_tiempo_vivo:
            max_tiempo_vivo= tiempo_vivo
        if current_distance> best_distance:
            best_distance=current_distance
        current_distance=0
        tiempo_vivo=0
        tubos= [Tubo(600, tubo_arriba, tubo_abajo), Tubo(600 + pipe_distance, tubo_arriba, tubo_abajo), Tubo(600 + 2 * pipe_distance, tubo_arriba, tubo_abajo),]


    #Estadisiticas:
    panel_width = 250
    panel_x = width - panel_width
    pygame.draw.rect(screen, (0, 0, 0), (panel_x, 0, panel_width, height))

    font_titulo = pygame.font.SysFont("Century Gothic", 30, bold=False)
    titulo = font_titulo.render("GA Statistics", True, (255, 197, 211))
    screen.blit(titulo, (panel_x + 40, 10))

    font = pygame.font.SysFont("Arial", 14)
    texto = font.render(f"Generation:  {generacion}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 60))

    texto = font.render(f"Alives:  {len(poblacion_viva)}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 80))

    texto = font.render("Prev Gen 2min:  ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 100))

    texto = font.render(f"Speed:  {speed}X ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 120))

    current_distance += 1
    texto = font.render(f"Current Distance:  {current_distance}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 160))

    #Mejor Distancia:
    mejor_distancia = max(p.rendimiento for p in poblacion.pobl)
    texto = font.render(f"Best Distance:  {best_distance} ", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 180))

    texto = font.render(f"Current Survival:  {tiempo_vivo / fps:.2f}s", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 220))

    texto = font.render(f"Best time:  {max_tiempo_vivo/ fps:.2f}s", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 240))

    texto = font.render(f"120s Survivors:  {survivors_120s}", True, (250,250,250))
    #texto = font.render(f"Last Gen Survival: {max_tiempo_vivo / fps:.2f}s", True, (250,250,250))
    screen.blit(texto, (panel_x + 20, 260))
       
    texto = font.render(f"Avg Distance Prev. Gen:  {promedio}", True, (250, 250, 250))
    screen.blit(texto, (panel_x + 20, 200))
    
    dibujar_genoma(screen, poblacion_viva, panel_x+20, 300)
    
    clock.tick(fps)
    pygame.display.update()

pygame.quit()