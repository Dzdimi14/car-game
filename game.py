#http://rmgi.blog/pygame-2d-car-tutorial.html

import os, time, pygame

from math import sin, radians, degrees, copysign
from car import Car
from track import Track
from pygame.math import Vector2


pygame.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(image_path)

default_width = 1280
default_height = 720

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0, 255, 0)
font = pygame.font.Font('freesansbold.ttf', 25)

check1_b = False #GLOBAL
check2_b = False
finish_b = False
lap = 0 #GLOBAL

#Global 
starttime = time.time() #GLOBAL
lasttime = 0
laptime = 0
laptimes = []

paused = False

class Game:

    def __init__(self):
        pygame.display.set_caption("Vroom Vroom Bitches")
        #global font
        self.font = font
        width = default_width
        height = default_height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        #spawn car
        spawn_position = (120, 480)
        self.car = Car(120, 480, 90.0)
        self.track = Track()



#### lap counting 

    def lap_count(self):
        global lap
        font = self.font.render("Lap: "+ str(lap), True, white)
        self.screen.blit(font, (0,0))

    def best_lap(self):
        if laptimes:
            best = min(laptimes)
            mesg = self.font.render("Best lap: " + str(best), True, white)
            self.screen.blit(mesg, (500, 0))

    def timer(self): #uses own display update for speed
        ticks = pygame.time.get_ticks()
        millisec = ticks % 1000
        seconds = int(ticks/1000 % 60)
        minutes = int(ticks/60000 % 60)
        msg = self.font.render('{minutes:02d}:{seconds:02d}:{millisec}'.format(minutes=minutes, millisec = millisec, seconds = seconds), True, white)
        self.screen.blit(msg, (100,0))
        pygame.display.update()


##DONT TOUCH THIS BLESSED GARBAGIO
    def finish_check(self, car):
        global finish_b, check1_b, check2_b, lap, starttime, lasttime, laptime
        check1 = pygame.Rect((1100, 384), (120, 5)) 
        check2 = pygame.Rect((520, 384), (5, 300))
        finish = pygame.Rect((60,384), (120, 5))
        
        if finish.collidepoint(car.position):
                finish_b = True
                print("fin")
        if check1.collidepoint(car.position):
                check1_b = True
                check2_b = False
                finish_b = False
                print("chk1")
        if check2.collidepoint(car.position):
                check2_b = True
                finish_b = False
                print("chk2")              
        if check1_b:
            if check2_b:
                if finish_b:
                    lap += 1
                    totaltime = round((time.time() - starttime), 2)
                    laptime = round(totaltime - lasttime, 2)
                    laptimes.append(laptime)

                    print("laptime :"+ str(laptime))
                    print("lasttime :" + str(lasttime))
                    lasttime += laptime

                    print("lap!")
                    finish_b = False
                    check1_b = False
                    check2_b = False
        msg1 = self.font.render("lap: "+ str(lap) + "time: "+ str(laptime), True, white)
        self.screen.blit(msg1,(300,0))









# wannabe GUI

    def message_display(self, text, size, coords):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurface, TextRect = self.text_objects(text, largeText)
        TextRect.center = coords
        self.screen.blit(TextSurface, TextRect)
        pygame.display.update()
        #time.sleep(2)        

    def text_objects(self, text, font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()



#### TODO
#
#s -escape makes you go back to esc screen

#
#
#
#
#
#s
#
#
#
#
#
####   
    def quit_game(self):
        pygame.quit()
        quit()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(self.screen, ac,( x, y, w, h), 5)
                if click[0] and action != None:
                    action()
            else:
                pygame.draw.rect(self.screen, ic,( x, y, w, h), 5)
            

            button_txt = pygame.font.Font('freesansbold.ttf', int(h/3))
            textSurf, textRect = self.text_objects(msg, button_txt)
            textRect.center = (x + (w / 2)), (y + (h / 2))
            
            self.screen.blit(textSurf, textRect)
            




    def intro_screen(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    pygame.quit()
                    quit()
            


            largeText = pygame.font.Font('freesansbold.ttf', 80)
            TextSurf, TextRect = self.text_objects("Vroom Vroom Bitches", largeText)
            TextRect.center = ((default_width/2),(default_height - default_height  * .66))
            self.screen.blit(TextSurf,TextRect)


            button_width = 200
            button_height = 100

            x1,y1 = (default_width/4), (default_height - default_height/4)
            x2,y2 = (default_width - default_width/4) - button_width, (default_height - default_height/4) 
            
            self.button("Vroom", x1, y1, button_width, button_height, white, green, self.run)
            self.button("Bye Bitch", x2, y2, button_width, button_height, white, red, self.quit_game)
            pygame.display.update()

    def unpause(self):
        global paused 
        paused = False
                                       

    def pause(self):
        #paused = True
        self.screen.fill(black)
        pause = True


        while pause:
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    pygame.quit()
                    quit()

            self.screen.fill(black)
            bw = 200
            bh = 100
            x,y = default_width/2 - bw/2,default_height * .5
            x1,y1 = default_width/2 - bw/2, default_height *.5 + bw
            
            self.button("Resume", x, y, 200, 100, white, green, self.unpause)
            self.button("Resume", x, y, 200, 100, white, green, self.run)
            self.button("Exit", x1, y1, 200, 100, white, red, self.quit_game)


            self.message_display("Paused", 80, (int(default_width/2), int(default_height - default_height * .75)))

            
            pygame.display.update()
            

    def crash(self):
        self.message_display("YOU CRASHED", 80, (int(default_width/2), int(default_height/2)))
        time.sleep(2)
        self.car.reset()
        self.run()


    def draw_track(self, track):
        for n in track:
            xy1 = n[0]
            xy2 = n[1]
            pygame.draw.line(self.screen, white, xy1, xy2, Track.line_thickness)
                        


####MAIN LOOOP#######
    
    def run(self):
        global paused
        car = self.car
        
        
        #GAME LOOOP###
        while not self.exit:
            #deltatime
            dt = self.clock.get_time() /1000

            self.timer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                
            
            # user input
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_ESCAPE]:
                paused = True
                self.pause()
            #Logic
            car.update(dt)

            #accelerate and brake
            car.accelerate((pressed), dt)
            car.brake((pressed), dt)
            car.steer((pressed), dt)


            #drawing
            self.screen.fill((0, 0, 0))

            #start finish
            pygame.draw.line(self.screen, red, (60, 384), (180, 384), 10) 
            track = Track.track1
            self.draw_track(track)

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
             
            ###### MAP STUFF
            #outerbounds of 
            if car.position.x < track_limLeft or car.position.x > track_limRight:
                self.crash()
            elif car.position.y > track_limitBot or car.position.y < track_limitTop:
                self.crash()
            #innerbounds
            elif (car.position.x > track_inLeft and car.position.x < track_inRight) and (car.position.y < track_inBot and car.position.y > track_inTop):
                self.crash()

            #finishline code

            self.finish_check(car)
            self.lap_count()
            self.best_lap()
            
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            
            #draw car
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))

            ppu = 10 #pixels per unit ratio
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            
            self.clock.tick(self.ticks)
            pygame.display.flip()

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.intro_screen()
    
