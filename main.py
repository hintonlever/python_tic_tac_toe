# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 15:04:12 2021

@author: Benji
"""

import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    K_1,
    K_KP0,                 # keypad 0
    K_KP1,                 # keypad 1
    K_KP2,                 # keypad 2
    K_KP3,                 # keypad 3
    K_KP4,                 # keypad 4
    K_KP5,                 # keypad 5
    K_KP6,                 # keypad 6
    K_KP7,                 # keypad 7
    K_KP8,                 # keypad 8
    K_KP9,                 # keypad 9
)



# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize pygame
pygame.init()
# Need this for text
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)
# Setup the clock for a decent framerate
clock = pygame.time.Clock()


# How to set default values:
    # https://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python

class Piece(pygame.sprite.Sprite):
    def __init__(self, pos = None, piece_type = None):
        super(Piece, self).__init__()
        
        if pos is None:
             pos = []
        self.pos = pos
        
        if piece_type is None:
            piece_type = 1
        self.piece_type = piece_type
        # Simple rectangle
        # self.surf = pygame.Surface((75, 25))
        # self.surf.fill((255, 255, 255))
               
        # Using an image
        # the .convert() call optimizes the Surface, making future .blit() calls faster.
        if piece_type == 1:    
            self.surf = pygame.image.load("cross.jpg").convert()
        else:
            self.surf = pygame.image.load("circle.jpg").convert()
            
        self.surf = pygame.transform.scale(self.surf,(180,180))
        # Reverse image
 
        centers = [
            (100,500),
            (300,500),
            (500,500),
            
            (100,300),
            (300,300),
            (500,300),
            
            (100,100),
            (300,100),
            (500,100)
            ]
        
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center = centers[pos-1])


class Board():
    def __init__(self):
        self.turn = 1
        self.board = [0,0,0,0,0,0,0,0,0]
        self.pieces = pygame.sprite.Group()
        self.game_over = False
        
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        
    def position_filled(self,pos):
        return(self.board[pos-1] > 0)
    
    def check_game_over(self):
        # All pieces filled
        if sum(x > 0 for x in self.board) == 9: self.game_over = True
        
        # HORZ rows
        if self.board[1-1] > 0 and self.board[1-1] == self.board[2-1] and self.board[2-1] == self.board[3-1]: self.game_over = True
        elif self.board[4-1] > 0 and self.board[4-1] == self.board[5-1] and self.board[5-1] == self.board[6-1]: self.game_over = True
        elif self.board[7-1] > 0 and self.board[7-1] == self.board[8-1] and self.board[8-1] == self.board[9-1]: self.game_over = True
        
        # VERT rows
        elif self.board[1-1] > 0 and self.board[1-1] == self.board[4-1] and self.board[4-1] == self.board[7-1]: self.game_over = True
        elif self.board[2-1] > 0 and self.board[2-1] == self.board[5-1] and self.board[5-1] == self.board[8-1]: self.game_over = True
        elif self.board[3-1] > 0 and self.board[3-1] == self.board[6-1] and self.board[6-1] == self.board[9-1]: self.game_over = True  
        
        # DIAG rows
        elif self.board[1-1] > 0 and self.board[1-1] == self.board[5-1] and self.board[5-1] == self.board[9-1]: self.game_over = True
        elif self.board[3-1] > 0 and self.board[3-1] == self.board[5-1] and self.board[5-1] == self.board[7-1]: self.game_over = True  
        
    def add_piece(self,pos):

        if self.position_filled(pos) == False and self.game_over == False:
           piece = Piece(pos,self.turn)
           self.pieces.add(piece)
           self.board[pos-1] = self.turn
           self.check_game_over()
           self.change_turn()
           
    def avail_moves(self):
        # This is 1 indexed
        return([int(i) + 1 for i, e in enumerate(self.board) if e == 0] )
        
class Turn(pygame.sprite.Sprite):
    def __init__(self):
        super(Turn, self).__init__()
        self.turn = 1
        self.turn_text = "Cross"
        self.surf = myfont.render(str("Cross"), False, (0,0,0))
        self.rect = self.surf.get_rect(center = (800,50))
        
    def update(self,turn):
        self.turn = turn
        if self.turn == 1:
            self.turn_text = "Cross"
        else:
            self.turn_text = "Nought"
        self.surf = myfont.render(self.turn_text, False, (0,0,0))
        self.rect = self.surf.get_rect(center = (800,50))
    
    
class Random_Bot():
    def __init__(self):
        self.ignore = 1
    
    def make_move(self,board):
        my_moves = board.avail_moves()
        my_move = random.choice(my_moves)
        board.add_piece(my_move)


# test = Piece()

# pieces.add(test)

board = Board()
turn = Turn()
random_bot = Random_Bot()


# Restart button
# defining a font

button_restart_text = myfont.render('RESTART' , True , (255,255,255))
color_light = (170,170,170)
color_dark = (100,100,100)
  

# Run until the user asks to quit
running = True
while running:
    
    # INIT STUFF
    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    # Vert lines for board
    pygame.draw.line(screen,"grey",(200,20),(200,580))
    pygame.draw.line(screen,"grey",(400,20),(400,580))  
    
    # Horz lines for board
    pygame.draw.line(screen,"grey",(20,200),(580,200))
    pygame.draw.line(screen,"grey",(20,400),(580,400))  
    
    pygame.draw.line(screen,"black",(600,0),(600,600)) 
    
    
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    
    if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
        pygame.draw.rect(screen,color_light,[SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])
        
   # superimposing the text onto our button
    screen.blit(button_restart_text , (SCREEN_WIDTH/2+50,SCREEN_HEIGHT/2)) 
        
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
                
        #checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
              
            #if the mouse is clicked on the
            # button the game is terminated
            if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
                pygame.quit()
                  
        
        if event.type == KEYUP and board.game_over == False:
            if event.key == K_KP1: board.add_piece(1)
            if event.key == K_KP2: board.add_piece(2)
            if event.key == K_KP3: board.add_piece(3)
            if event.key == K_KP4: board.add_piece(4)
            if event.key == K_KP5: board.add_piece(5)
            if event.key == K_KP6: board.add_piece(6)
            if event.key == K_KP7: board.add_piece(7)
            if event.key == K_KP8: board.add_piece(8)
            if event.key == K_KP9: board.add_piece(9)

          
    
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    
  

    
   
       # Update score
    turn.update(board.turn)
    screen.blit(turn.surf,turn.rect)
                
    if board.turn == 1:
        random_bot.make_move(board)
       
    # Draw all sprites
    for piece in board.pieces:
        screen.blit(piece.surf, piece.rect)
    
    
    
    
    # if board.game_over == True:
    #     print("Game Over")
    
    # Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
  

    
# Done! Time to quit.
pygame.quit()