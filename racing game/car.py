
import os
from math import sin, radians, degrees, copysign
import pygame
from pygame.math import Vector2



class Car:

    def __init__(self, x, y, angle =90.0, length = 4, max_steering = 15, max_acceleration = 30.0):
        self.x = x
        self.y = y
        self.position = Vector2(self.x, self.y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.steering_rate = 5

        self.acceleration = 10
        self.acceleration_factor = 2.71828 # e
        self.steering = 1

        self.brake_deceleration = max_acceleration


    def reset(self):
        self.x = 120
        self.y = 480
        self.position = Vector2(120, 480)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 90.0
        print(self.position)

    def accelerate(self, pressed, dt):
        
        if pressed[pygame.K_UP]:
            self.acceleration += self.acceleration_factor * dt
        else:
            self.acceleration = 0
            #self.velocity -= (self.velocity / 55) #friction

        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    def brake(self, pressed, dt):
        if pressed[pygame.K_DOWN]:
            self.acceleration = -self.brake_deceleration
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    def steer(self, pressed, dt):
        if pressed[pygame.K_RIGHT]:
            self.steering -= self.steering_rate * dt
        elif pressed [pygame.K_LEFT]:
            self.steering += self.steering_rate * dt
        else:
            self.steering = 0
            #TODO make it more realistic with no input
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))


    def update(self, dt):
        #velocity modifier to make car feel lighter
        mod = 1

        ###B R O K E N
       # print("velocity :" + str(self.velocity))
       # print("acceleration :" + str(self.acceleration))
        self.velocity += (self.acceleration * dt, 0) #dt - the amount of seconds passed since last frame
        ###B R O K E N
        self.velocity -= self.velocity / 600  # friction
        #print(self.acceleration)
        
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        


         