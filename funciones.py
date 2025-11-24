import pygame

def paso_tubo(pajaro, tubos, playerImg):
    #player_hit = pygame.Rect(pajaro.coordp[0],pajaro.coordp[1],playerImg.get_width(),playerImg.get_height(),)
    player_hit = pygame.Rect(pajaro.coordp[0], pajaro.coordp[1],
                         playerImg.get_width(), playerImg.get_height())
    #mueren si tocan los tubos
    for tubo in tubos:
        if player_hit.colliderect(tubo.rect_arriba) or player_hit.colliderect(tubo.rect_abajo):
            return False
    return True

def tubo_cercano(pajaro, tubos):
    tubos_adelante=[]
    for tubo in tubos:
        if tubo.x + tubo.ancho > pajaro.coordp[0]:
            tubos_adelante.append(tubo)
    if len(tubos_adelante)==0:
        return tubos[-1] #si no tiene ninguno adelante devuelve el ultimo
    else:
        return min(tubos_adelante, key=lambda t: t.x) #devuelve el mas cercano

