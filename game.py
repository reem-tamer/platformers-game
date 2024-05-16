import pygame
import random
import os
import csv



from sys import exit
pygame.init()
pygame.display.set_caption("Kings and Pigs")
screen_width= 800
screen_hight= 640
window= pygame.display.set_mode((screen_width,screen_hight))

FPS= 60
king_velocity= 5

#setting the images
background= pygame.image.load("background.png")
bar=pygame.image.load("bar.png")
#def main(window):
clock=pygame.time.Clock()
run= True
while run:
    clock.tick(FPS)
    window.fill((0,0,0))
    window.blit(background,(0,0))
    window.blit(bar,(400,320))
    window.blit(bar,(250,380))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()



