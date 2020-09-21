
import pygame
import time
import random


#INIT
pygame.init() #initialyze pygame

display_height = 600
display_width = 800

car_width = 80

#RGB COLORS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255) 


gameDisplay = pygame.display.set_mode((display_width, display_height)) 
pygame.display.set_caption('a lil racey')

clock = pygame.time.Clock()



carImg = pygame.image.load('car.png')

def obs_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0, 0))

def obstacles(x_loc, y_loc, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x_loc, y_loc, w, h])

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def crash():
    message_display('YOU CRASHED :(')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 80) #font and size
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height / 2))
    gameDisplay.blit(TextSurface, TextRect)

    pygame.display.update()

    time.sleep(3)
    game_loop()



def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    gameExit = False 
    
    x_change = 0

    obstacle_startx = random.randrange(0, display_width)
    obstacle_starty = -600
    obstacle_speed = 6
    obs_h = 100
    obs_w = 100

    dodged = 0

    while not gameExit:
        for event in pygame.event.get(): #searches for event from user
           if event.type == pygame.QUIT: #if user quits
               pygame.quit()
               quit()
           if event.type == pygame.KEYDOWN: #keypress left or right arrows
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
           if event.type ==pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        #paint
        gameDisplay.fill(white)
        obstacle_starty += obstacle_speed 
        obstacles(obstacle_startx, obstacle_starty, obs_w, obs_h, black)
        car(x,y)
        obs_dodged(dodged)

        if x > (display_width - car_width) or x < (0 - car_width):
            crash()

        if obstacle_starty > display_height: #has obs passed screen?
            dodged += 1
            obs_w += (dodged * 1.13)
            obstacle_speed += (dodged * 0.1)
            obstacle_starty = 0 - obs_h
            
            obstacle_startx = random.randrange(0,display_width)
            
        if y < obstacle_starty + obs_h:
            if x > obstacle_startx and x < obstacle_startx + obs_w or x + car_width > obstacle_startx and x + car_width < obstacle_startx + obs_w:
                crash()



        pygame.display.update()
        clock.tick(60)       #60 ticks per second


game_loop()
pygame.quit()
quit()