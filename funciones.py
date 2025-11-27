import pygame

def paso_tubo(pajaro, tubos, playerImg):
    #player_hit = pygame.Rect(pajaro.coordp[0],pajaro.coordp[1],playerImg.get_width(),playerImg.get_height(),)
    player_hit = pygame.Rect(pajaro.coordp[0]+5, pajaro.coordp[1]+5,
                         playerImg.get_width()-10, playerImg.get_height()-10)
    #mueren si tocan los tubos
    for tubo in tubos:
        if player_hit.colliderect(tubo.rect_arriba) or player_hit.colliderect(tubo.rect_abajo):
            return False
    return True

def dibujar_genoma(screen, poblacion, x, y):
    """
    Dibuja barras simples mostrando el promedio de cada peso w0..w5
    """
    fuente = pygame.font.SysFont("arial", 16)
    ancho_max = 70
    espacio = 25

    lista_w = list(zip(*[p.w for p in poblacion]))

    for i, pesos in enumerate(lista_w):

        prom = sum(pesos) / len(pesos)

        barra = int((prom / 5) * ancho_max)

        by = y + i * espacio

        txt = fuente.render(f"w{i}:", True, (255, 255, 255))
        screen.blit(txt, (x, by))

        pygame.draw.line(screen, (80, 80, 80), (x + 100, by + 10), (x + 100 + ancho_max, by + 10), 2)
        pygame.draw.line(screen, (80, 80, 80), (x + 100, by + 10), (x + 100 - ancho_max, by + 10), 2)

        color = (0, 200, 0) if prom > 0 else (200, 50, 50)

        if barra >= 0:
            pygame.draw.rect(screen, color, (x + 100, by + 5, barra, 10))
        else:
            pygame.draw.rect(screen, color, (x + 100 + barra, by + 5, -barra, 10))

        val = fuente.render(f"{prom:.2f}", True, (255, 255, 255))
        screen.blit(val, (x + 180, by))
