import numpy as np
import sys
import random
import pygame
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

import os

 
SCREEN_WIDTH=160
SCREEN_HEIGH=320
FPS =60



MAX_CARS_COUNT = 10
CAR_ATTRIBUTE_COUNT =4 # x , y , sx , sy
MIN_SPEED = 7/10
MAX_SPEED =  7/10


AGENT_INIT_SPEED = 0/10  
AGENT_MAX_SPEED = 10/10  

TILE_SIZE =16

WORD_WIDTH = 9 * TILE_SIZE 
WORD_HEIGHT = 19 * TILE_SIZE 
 
pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGH), pygame.RESIZABLE)
pygame.display.set_caption("Simuator")


 
bg_image  = pygame.image.load("data/bg.png").convert_alpha()
car_image = pygame.image.load('data/black.png').convert_alpha()
 

clock = pygame.time.Clock()

starts = [
    {'y': 0 *TILE_SIZE, 'x': 3 *TILE_SIZE, 'start': 'down'},
    {'y': 0*TILE_SIZE , 'x': 4*TILE_SIZE , 'start': 'down'},
    {'y': 19 *TILE_SIZE, 'x': 5*TILE_SIZE , 'start': 'up'},
    {'y': 19 *TILE_SIZE, 'x': 6 *TILE_SIZE, 'start': 'up'}
]  

agent_start = {'y': 10*TILE_SIZE, 'x': -1*TILE_SIZE, 'start': 'right'}


class GameState:
    def __init__(self):
        self.state = np.zeros((MAX_CARS_COUNT, CAR_ATTRIBUTE_COUNT))
        self.car_count =1
        self.reset_agent()
        self.score = 0
 
    def frame_step(self ,input_actions):
        clock.tick(FPS)
        reward=0.1      
        terminal =False
        
        if input_actions[1] == 1:
            # increment speed
            self.state[0,2]+=0.01
            if self.state[0,2] > AGENT_MAX_SPEED :
                self.state[0,2]=AGENT_MAX_SPEED 
        if input_actions[2] == 1:
            # decrement speed
            self.state[0,2]+=0.01
            if self.state[0,2] < 0 :
                self.state[0,2]=0
       
        #logic
        if self.car_count < MAX_CARS_COUNT  :
            self.generate_cars()



        self.move_cars()
        self.reset_cars()


        agent = self.state[0]


        if agent[2]==0 :
            reward = 0 
       
        if agent[0] > WORD_WIDTH :
            self.reset_agent()
            reward =1
            self.score += 1


        if self.detect_collision():
            self.reset_agent()
            terminal =True
            reward = -1
            self.score = 0

        
        #drawing
        SCREEN.blit(bg_image, (0,0))
        for i  in range(self.car_count) :
            car = self.state[i]
            SCREEN.blit(car_image, (car[0],car[1]))
        

        pygame.display.set_caption(str(self.state[0,2]))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        
        

        return image_data , reward , terminal , self.score

    

    def move_cars(self):
        for i  in range(self.car_count) :
            car = self.state[i]
            car[0]+=car[2]
            car[1]+=car[3]  


    
    def reset_agent(self):
        car = self.state[0]
        car[0]=agent_start["x"]
        car[1]=agent_start["y"]

        car[2] =AGENT_INIT_SPEED 
        car[3]= 0

    def generate_cars(self):
        if random.randint(0, 1000) < 996:
            return

        self.reset_car(self.car_count)
        self.car_count+=1


    def reset_car(self , id ):
        


        car = self.state[id]
        start = random.choice(starts) 
        car[0]=start["x"]
        car[1]=start["y"]

        car[2] , car[3] =self.generate_velocity(start)
 

     
    def reset_cars(self):
        for i  in range(1,self.car_count) :
            car = self.state[i]
            if car[1] > WORD_HEIGHT :
                self.reset_car(i) 
            if car[1] < 0 :
                self.reset_car(i) 

 
    def generate_velocity(self , start):
        velocity = 0.7# random.uniform(MIN_SPEED, MAX_SPEED)
        if start["start"] == "up":
            return 0,- velocity 

        if start["start"] == "down":
            return 0, velocity 


    def detect_collision(self):
        c1 =self.state[0]
        for i  in range(1,self.car_count) :
            c2 = self.state[i]
            if check_car_collision(c1,c2) :
                return True
        return False


CAR_WIDTH=16
CAR_HEIGHT=16

def check_car_collision(car1, car2):
    return not (car1[0] > car2[0] + CAR_WIDTH or car1[0] + CAR_WIDTH < car2[0] or car1[1] > car2[1]+CAR_HEIGHT or car1[1]+CAR_HEIGHT < car2[1])



if __name__ == "__main__":
   
    
    try:
        game = GameState()
        while True:
             game.frame_step(None)
    except:
        pygame.quit()
        raise


