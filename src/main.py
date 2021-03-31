import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


pygame.init()
SCREEN_W = 800
SCREEN_H = 600
WHITE = (255,255,255)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
running = True

class Pop(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Pop, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(color)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    pop = Pop((0,0,255))
    screen.blit(pop.surf, (250, 250))
    pygame.display.flip()

pygame.quit()
