import pygame
#hitbox: parte invisible para detectar colisiones
def paso_tubo(pajaro, tubos, playerImg): #comprueba sie l pájaro choca algún tubo, si no choca entonces True
    #player_hit = pygame.Rect(pajaro.coordp[0],pajaro.coordp[1],playerImg.get_width(),playerImg.get_height(),)
    player_hit = pygame.Rect(pajaro.coordp[0]+5, pajaro.coordp[1]+5, 
                         playerImg.get_width()-10, playerImg.get_height()-10) #reduce falsos positivos
    #si el hitbox del pájaro toca el hitbox de los tubos, muere el pájaro
    for tubo in tubos:
        if player_hit.colliderect(tubo.rect_arriba) or player_hit.colliderect(tubo.rect_abajo): #devuelve True si los rectangulos se superponen
            return False #como es True que se superponen rectángulos, devuelve Falseporque el pájaro NO pasó
    return True #si terminó el fro y no detectó colisiones/superposiciones devuelve True (el pájaro sí pasó)

def dibujar_genoma(screen, poblacion, x, y):
    """
    Dibuja barras simples mostrando el promedio de cada peso w0..w5
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
