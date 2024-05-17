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


#create platform bars main class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create platforms using sprite groups, putting each bar in its position
platforms = pygame.sprite.Group()
platforms.add(Platform(400, 320, 'bar.png'))
platforms.add(Platform(250, 380, 'bar.png'))
platforms.add(Platform(100, 300, 'bar.png'))
platforms.add(Platform(570, 185, 'bar.png'))
platforms.add(Platform(570, 280, 'bar.png'))
platforms.add(Platform(400, 230, 'bar.png'))






#main game loop

clock=pygame.time.Clock()
run= True

while run:

    clock.tick(FPS)
    window.fill((0,0,0))
    window.blit(background,(0,0))

#"blitting" the bars but instead of using blit we use draw
    # since it is a function related to sprite groups
    platforms.draw(window)















   # to exit the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()






