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
ground= screen_hight-140

score_font= pygame.font.Font('Pixeltype.ttf',50)


#setting the images
background= pygame.image.load("background.png").convert_alpha()
background2 = pygame.image.load("background2.jpg").convert_alpha()
bar=pygame.image.load("bar.png").convert_alpha()
run_img = pygame.image.load('Run.png').convert_alpha()
jump_img = pygame.image.load('Jump.png').convert_alpha()
jump_size = pygame.transform.scale(jump_img,(60,60))
idle_img = pygame.image.load('Idle2.png').convert_alpha()
fall_img = pygame.image.load('Fall (78x58).png').convert_alpha()
pig_idle = pygame.image.load('Idle_pig.png').convert_alpha()
pig_run = pygame.image.load("Run (34x28).png").convert_alpha()
diamond_img = pygame.image.load("diamond.png").convert_alpha()
close= pygame.image.load("closed_door.png").convert_alpha()
opening= pygame.image.load("opening_door.png").convert_alpha()
heart_original= pygame.image.load("heart.png").convert_alpha()
heart=pygame.transform.scale(heart_original, (50, 40))


#create platform bars main class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)




# creating main player class
#under the assumption of idle initial position
# other pos itions will be updated later
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 71
        self.height = 54

        self.image = idle_img
        self.king_size=pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.king_size.get_rect() #transform image in the line before
                                            #to rect
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
        self.running = False
        self.jumping = False
        self.falling = False
        self.direction = 1
        self.score = 0
        self.lives= 3
        self.initial_x = x
        self.initial_y =y

        #update keys to move the king,
        # function parameters include platform
        # so we can later on check for collisions with the bars

    def update(self, platforms , diamonds):
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
            self.image = jump_size
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

        # to keep the king within the floor boundry of the game
        if self.rect.y >= ground:
            self.rect.y = ground
            self.vel_y = 0
            self.on_ground = True
            self.falling = False

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground and self.rect.y + king_velocity >= 140:
            self.vel_y = jump_strength
            self.jumping = True
        else:
            self.jumping = False

            # floor boundary so king doesnt fall


    # collision with diamonds
        for diamond in diamonds:
            if self.rect.colliderect(diamond.rect):
                self.score += 1
                diamond.kill()

#reseting the position for the king
        #this function returnd the king rect to the starting position and  gives it velocity zero
    def reset_position(self):
        self.rect.topleft = (self.initial_x, self.initial_y)
        self.velocity_y = 0

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y,width,height):
        super().__init__()
        self.image = pygame.transform.scale(diamond_img, (width, height))
        # self.image = diamond_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


king= Player(400,110)

#we are doing a class for the door
# so it opens when the player collects all 5 diamonds in the platform
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_closed = close
        self.image_open = opening
        self.image = self.image_closed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.open = False

    def update(self, player):
        if player.score == 5:
            self.image = self.image_open
            self.open = True
        else:
            self.image = self.image_closed
            self.open = False
        if self.open and king.rect.colliderect(self.rect):
            king.kill()


class Pig(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,right_boundary,left_boundary):
        super().__init__()
        self.image = pygame.transform.scale(pig_idle, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 1  # Pig moves right and left
        self.speed = 1.5
        self.left_boundary= left_boundary
        self.right_boundary= right_boundary




    def update(self):
        self.rect.x += self.direction * self.speed
        # # Reverse direction if the pig hits the screen edges
        # if self.rect.right >= screen_width - 120 or self.rect.left <= 120:
        #     self.direction *= -1
        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.direction *= -1


pig = Pig(200,490,60,60,300,120) #fly
pig2 = Pig(100,400,60,60,680,120)
pig3 = Pig(300,200,60,60,680,120)
door = Door(110, 290)

diamond= Diamond(100,200,20,20)


# Create platforms using sprite groups, putting each bar in its position
platforms = pygame.sprite.Group()
platforms.add(Platform(400, 340, 'bar.png')) #1
platforms.add(Platform(250, 440, 'bar.png')) #2 lowest bar
platforms.add(Platform(100, 350, 'bar.png')) #3
# platforms.add(Platform(570, 160, 'bar.png'))
platforms.add(Platform(570, 270, 'bar.png')) #5
platforms.add(Platform(400, 180, 'bar.png')) #6
#variable called all sprites and add to it the king and all the platforms
all_sprites = pygame.sprite.Group()
all_sprites.add(king)
all_sprites.add(pig)
all_sprites.add(*platforms)
all_sprites.add(door)

# Creating the diamonds for the king to catch
diamonds = pygame.sprite.Group()
diamonds.add(Diamond(450, 310,30,30)) #on bar1
diamonds.add(Diamond(300, 410,30,30))# on bar2
diamonds.add(Diamond(600, 500,30,30)) # on floor
diamonds.add(Diamond(600, 240,30,30))
diamonds.add(Diamond(200, 500,30,30))# on floor
all_sprites.add(*diamonds)

# creating level 1
def level1():
    platforms.empty() #emptying the past setup to ensure a new one for the next level
    diamonds.empty()
    all_sprites.empty()
#then re adding our new elements in the level
    platforms.add(Platform(400, 340, 'bar.png'))
    platforms.add(Platform(250, 440, 'bar.png'))
    platforms.add(Platform(100, 350, 'bar.png'))
    platforms.add(Platform(570, 270, 'bar.png'))
    platforms.add(Platform(400, 180, 'bar.png'))

    diamonds.add(Diamond(450, 310, 30, 30))
    diamonds.add(Diamond(300, 410, 30, 30))
    diamonds.add(Diamond(600, 500, 30, 30))
    diamonds.add(Diamond(600, 240, 30, 30))
    diamonds.add(Diamond(200, 500, 30, 30))

    door.rect.topleft = (110, 290)
    pig2.rect.topleft = (200, 490)

#re adding the sprite groups on the screen
    all_sprites.add(door)
    all_sprites.add(king)
    all_sprites.add(pig2)

    all_sprites.add(*platforms)
    all_sprites.add(*diamonds)



def level2():
    platforms.empty()
    diamonds.empty()
    all_sprites.empty()

    platforms.add(Platform(130, 430, 'bar.png')) #bar2
    platforms.add(Platform(260, 430, 'bar.png'))#bar3
    platforms.add(Platform(530, 300, 'bar.png'))#bar1
    platforms.add(Platform(300, 360, 'bar.png'))#bar4


    diamonds.add(Diamond(470, 480, 30, 30))
    diamonds.add(Diamond(370, 330, 30, 30))
    diamonds.add(Diamond(195, 400, 30, 30))
    diamonds.add(Diamond(300, 400, 30, 30))
    diamonds.add(Diamond(550, 270, 30, 30))


    door.rect.topleft = (610, 490)
    pig.rect.topleft = (130,367)
    pig2.rect.topleft = (130, 485)
    pig3.rect.topleft = (300, 485)

    all_sprites.add(door)
    all_sprites.add(king)
    all_sprites.add(pig)
    all_sprites.add(pig2)
    all_sprites.add(pig3)

    all_sprites.add(*platforms)
    all_sprites.add(*diamonds)









#main game loop

clock=pygame.time.Clock()
game_won =False
run= True
level=1
level1() # we called the level1 function outside the while loop
# because by default we want to start at level1
while run:

    clock.tick(FPS)
    window.fill((0,0,0))
    if level==1:  # if its level1 call update function for pig1 and bg1
        window.blit(background,(0,0))
        pig.update()
    if level==2: #if its level2 call update bg2 and call all the pigs including level1 pig
        window.blit(background2,(0,0))
        pig.update()
        pig2.update()
        pig3.update()


#outside the if we called the king and door because they are common between 2 levels

    king.update(platforms, diamonds)
    door.update(king)
    all_sprites.draw(window)



#when the king rect collides wsith the pig rect
    # the lives decrease by one and the king goes back to initial position if it hits the pig 3 times
    # the game is over
    if king.rect.colliderect(pig2.rect) or (level == 2 and (king.rect.colliderect(pig.rect) or king.rect.colliderect(pig3.rect))):


        king.lives -= 1
        king.reset_position()
        lost_life_caption = score_font.render("Oops! you hit the pig", False, 'red')
        window.blit(lost_life_caption, (250, 300))
        pygame.display.update()
        pygame.time.delay(1000)

        if king.lives == 0:
            game_over_caption = score_font.render("Game Over!", False, 'red')
            window.blit(game_over_caption, (300, 200))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False  # Exit the game loop to end the game

        # Draw all sprites
    all_sprites.draw(window)
    #pygame.draw.rect(window, (255, 255, 255), king.rect, 1)

    # Draw hearts representing lives
    for i in range(king.lives):
         window.blit(heart, (90 + i * 50, 95)) #this equation to draw 3 hearts next to each other



    score_text = score_font.render(f"Diamonds: {king.score}", False, 'white')
    window.blit(score_text, (530, 110))

    if door.open and king.rect.colliderect(door.rect):
        if level==1: # if the level is already lecvel1 we change it to level 2
            winning_caption = score_font.render("leveled up!", False, 'green')
            window.blit(winning_caption, (150, 350))
            level=2
            king.score=0 #return the score to zero and lives 3
            king.lives=3
            king.reset_position() #reset the king position using king reset function
            level2() # call level2 function
        else:
            game_won = True # else the player is already in level2 and the whole game is won



    if game_won == True:
        winning_caption = score_font.render("Congratulations! You escaped the pig!", False, 'green')
        window.blit(winning_caption, (120, 300))


        pygame.display.update()
        pygame.time.delay(2000) #gives the player the chance to read the massege
        run = False

    else:
        pygame.display.flip()
    # to exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()


















