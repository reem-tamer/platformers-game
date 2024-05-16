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

class Bar(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("bar.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#def main(window):
clock=pygame.time.Clock()
run= True

while run:

    clock.tick(FPS)
    window.fill((0,0,0))
    window.blit(background,(0,0))
    window.blit(bar,(400,320))  #1
    window.blit(bar,(250,380))  #2
    window.blit(bar, (100, 300)) #3
    window.blit(bar, (570, 185)) #4
    window.blit(bar, (570, 280)) #5
    window.blit(bar, (400, 230)) #6

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()



