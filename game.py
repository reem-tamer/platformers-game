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
gravity= 0.6
jump_strength= -12


#setting the images
background= pygame.image.load("background.png").convert_alpha()
bar=pygame.image.load("bar.png").convert_alpha()
run_img = pygame.image.load('Run.png').convert_alpha()
jump_img = pygame.image.load('Jump.png').convert_alpha()
idle_img = pygame.image.load('Idle2.png').convert_alpha()
fall_img = pygame.image.load('Fall (78x58).png').convert_alpha()


#create platform bars main class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)




# creating main player class
#under the assumption of idle initial position
# other positions will be updated later
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 71
        self.hieght = 54
        self.image = idle_img
        self.rect = self.image.get_rect() #transform image in the line before
                                            #to rect
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
        self.running = False
        self.jumping = False
        self.falling = False

        #update keys to move the king,
        # function parameters include platform
        # so we can later on check for collisions with the bars

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.running = False

        if keys[pygame.K_LEFT] == True and self.rect.x - king_velocity >= 100:
            self.rect.x -= king_velocity
            self.running = True
        if keys[pygame.K_RIGHT] == True and king_velocity + self.rect.x <= 650:
            self.rect.x += king_velocity
            self.running = True

           # relation with past code and uploaded images
            # to change king state when he runs,jumps,falls
        if self.jumping == True:
            self.image = jump_img
        elif self.falling == True:
            self.image = fall_img
        elif self.running == True:
            self.image = run_img
        else:
            self.image = idle_img


        #gravity
        self.vel_y += gravity  # we add the variable gravity(0.6)
         # to the vertical position of the king
         # in order for it to return to the ground
        self.rect.y += self.vel_y

            #check if the king is in falling state or on ground
        self.on_ground = False
        self.falling = True

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down because when vel of y increase
                     # king gets closer to the ground
                    self.rect.bottom = platform.rect.top #if king is falling
                    # stop the fall and collide with platform
                    self.vel_y = 0
                    self.on_ground = True
                    self.falling = False
                elif self.vel_y < 0:  # vel<0 means king is jumping
                     # so if the top of the king rect comes in contact with the bar bottom
                    # return the king to the platform bottom
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Jump
        if keys[pygame.K_UP] and self.on_ground and self.rect.y + king_velocity >= 140:
            self.vel_y = jump_strength
            self.jumping = True
        else:
            self.jumping = False

king= Player(100,320)

# Create platforms using sprite groups, putting each bar in its position
platforms = pygame.sprite.Group()
platforms.add(Platform(400, 320, 'bar.png'))
platforms.add(Platform(250, 380, 'bar.png'))
platforms.add(Platform(100, 300, 'bar.png'))
platforms.add(Platform(570, 160, 'bar.png'))
platforms.add(Platform(570, 280, 'bar.png'))
platforms.add(Platform(400, 210, 'bar.png'))
#variable called all sprites and add to it the king and all the platforms
all_sprites = pygame.sprite.Group()
all_sprites.add(king)
all_sprites.add(*platforms)




#main game loop

clock=pygame.time.Clock()
run= True

while run:

    clock.tick(FPS)
    window.fill((0,0,0))
    window.blit(background,(0,0))

    # Update sprites
    all_sprites.update(platforms)



    # Draw all sprites
    all_sprites.draw(window)
    pygame.draw.rect(window, (255,255,255), king.rect, 1)

    # Refresh display
    pygame.display.flip()

    #"blitting" the bars but instead of using blit we use draw
    # since it is a function related to sprite groups
    # platforms.draw(window)
















   # to exit the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()






