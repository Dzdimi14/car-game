
import os
from math import sin, radians, degrees, copysign
import pygame
from pygame.math import Vector2



class Car:

    def __init__(self, x, y, angle =90.0, length = 4, max_steering = 15, max_acceleration = 30.0):
        self.x = x
        self.y = y
        self.position = Vector2(x, y)
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


    def accelerate(self, pressed, dt):
        
        if pressed[pygame.K_UP]:
            self.acceleration += self.acceleration_factor * dt

        elif pressed[pygame.K_DOWN]:
            self.acceleration -= self.acceleration_factor * dt
        else:
            self.acceleration = 0

        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))


    def brake(self, pressed, dt):
        #TODO brakes dont work, do same thing as letting go
        if pressed[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = copysign(self.max_acceleration, -self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if dt != 0:
                self.acceleration = -self.velocity.x /dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    def update(self, dt):
        #velocity modifier to make car feel lighter
        mod = 1

        self.velocity += (self.acceleration * dt * mod, 0) #dt - the amount of seconds passed since last frame
        #print(self.velocity)
        #print(self.acceleration)
        
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        


