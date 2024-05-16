import pygame
import random
import os


pygame.init()
pygame.display.set_caption("Kings and Pigs")
screen_width= 1000
screen_hight=1000
window= pygame.display.set_mode((screen_width,screen_hight))

FPS= 60
king_velocity= 5

def main(window):
    clock=pygame.time.Clock()
    run= True
    while run:
        clock.tick(FPS)
        window.fill((0,0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()

