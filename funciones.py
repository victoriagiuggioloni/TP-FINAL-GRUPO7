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

