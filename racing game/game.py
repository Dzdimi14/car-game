
#http://rmgi.blog/pygame-2d-car-tutorial.html



import os
import time
from math import sin, radians, degrees, copysign
from car import Car
from track import Track
import pygame
from pygame.math import Vector2

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(image_path)

default_width = 1280
default_height = 720

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255) 



class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Vroom Vroom Bitches")
        width = default_width
        height = default_height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False


    #TODO make lap counter work with timer
    def lap_count(self, count, lasttime):
                
        laptime = round((time.time() - lasttime), 2)

        font = pygame.font.Font('freesansbold.ttf',25)
        text = font.render("Lap: "+ str(count) + "Lap Time: " + str(laptime), True, white)
        

        self.screen.blit(text, (0,0))



    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurface, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((default_width/2),(default_height/2))
        self.screen.blit(TextSurface, TextRect)

        pygame.display.update()

        time.sleep(3)
        self.run()
        


    def text_objects(self, text, font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()


    def crash(self):
        self.message_display("YOU CRASHED")

        



    def run(self):
        lap_count = 0
        #spawn car
        spawn_position = (120, 480)
        car = Car(120, 480)
        track = Track()

        while not self.exit:
            dt = self.clock.get_time() /1000




            #EVENT queueueueeu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # user input
            pressed = pygame.key.get_pressed()
            
            #Logic
            car.update(dt)

            #accelerate and brake
            car.accelerate((pressed), dt)
            car.brake((pressed), dt)
            pressed = pygame.key.get_pressed()

            #steering
            if pressed[pygame.K_RIGHT]:
                car.steering -= car.steering_rate * dt
            elif pressed [pygame.K_LEFT]:
                car.steering += car.steering_rate * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            #drawing
            self.screen.fill((0, 0, 0))
            #Draw map

            ##TODO
            #function that automatically draws line of track
            pygame.draw.line(self.screen, white, (60, 36), (60, 684), 5)
            pygame.draw.line(self.screen, white, (60, 36), (1220, 36), 5)
            pygame.draw.line(self.screen, white, (60, 684),(1220, 684), 5)
            pygame.draw.line(self.screen, white, (1220, 684), (1220, 36), 5)

            pygame.draw.line(self.screen, white, (180, 156), (180, 576), 5)
            pygame.draw.line(self.screen, white, (180, 576), (1100, 576), 5)
            pygame.draw.line(self.screen, white, (1100, 156), (1100, 576), 5)
            pygame.draw.line(self.screen, white, (180, 156), (1100, 156), 5)
            
            #start finish
            pygame.draw.line(self.screen, red, (60, 384), (180, 384), 10) 

            #track collision boundaries
            track_limLeft = 60
            track_limRight = 1220
            track_limitTop = 36
            track_limitBot = 684

            track_inLeft = 180
            track_inRight = 1100
            track_inTop = 146
            track_inBot = 576

            start_finishY = 384
            
            #outerbounds
            if car.position.x < track_limLeft or car.position.x > track_limRight:
                self.crash()
            elif car.position.y > track_limitBot or car.position.y < track_limitTop:
                self.crash()
            #innerbounds
            elif (car.position.x > track_inLeft and car.position.x < track_inRight) and (car.position.y < track_inBot and car.position.y > track_inTop):
                self.crash()

            #lap counting

            starttime = time.time()
            lasttime = starttime
            
            if (car.position.x < track_inLeft and (round(car.position.y) == start_finishY)): #if we are on finish line
                lap_count = lap_count + 1 
                print("lap!")
                 
            self.lap_count(lap_count, lasttime)
            




            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
          
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))

            ppu = 10 #pixels per unit ratio
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            

            pygame.display.flip()
            self.clock.tick(self.ticks)


        pygame.quit()







if __name__ == '__main__':
    game = Game()
    game.run()


