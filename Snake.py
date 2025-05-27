import pygame, sys, random
from pygame.locals import *

# Things to implement
# - fix fruit spawns
# - add pause button
# - fix crash when doing a 180


pygame.init()

# Window Settings
window_width = 1500
window_height = 1000

# Creating Colours
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
grey = pygame.Color(128, 128, 128)
white = pygame.Color(255, 255, 255)

# Display Setup
DISPLAYSURF = pygame.display.set_mode((window_width,window_height))
background = Rect(0, 0, window_width, window_height)
background_surf = pygame.Surface((window_width, window_height))
background_surf.fill(black)

# Setting Framerate
FPS = 60
FramePerSec = pygame.time.Clock()

# Setting window title
pygame.display.set_caption("Game")

# Setting up fonts
score_font = pygame.font.SysFont("Comic_sans", 60)
high_score_font = pygame.font.SysFont("Comic_sans", 30, False, True)

tile_size = 50
margin = 4

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.x = 0
        self.y = 4
        self.prevx = self.x
        self.prevy = self.y
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = self.surf.get_rect(topleft=(self.x*tile_size, self.y*tile_size))
        self.surf.fill(green)
        self.dx = 1
        self.dy = 0
        
    def move(self):
        
        self.prevx = self.x
        self.prevy = self.y
        
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size
        
        # going over or under the vertical limits
        if (self.rect.y >= window_height):
            self.rect.y = margin*tile_size
            self.y = margin
        if (self.rect.y < margin*tile_size):
            self.rect.y = window_height
            self.y = window_height/tile_size 
        # going over or under the horizonal limits
        if (self.rect.right > window_width):
            self.rect.x = 0
            self.x = 0
        if (self.rect.left < 0):
            self.rect.x = window_width
            self.x = window_width/tile_size 
            
            
    def changeDirection(self):
        pressed_keys = pygame.key.get_pressed()
        if (self.dx == 0):
            if (pressed_keys[K_RIGHT]):
                self.dx = 1
                self.dy = 0
            elif (pressed_keys[K_LEFT]):
                self.dx = -1
                self.dy = 0
            
        if (self.dy == 0):
            if (pressed_keys[K_DOWN]):
                self.dx = 0
                self.dy = 1
            elif (pressed_keys[K_UP]):
                self.dx = 0
                self.dy = -1
          
     
Snake = Player() 
body = []    
body.append(Snake)
score = 0
        
class Body(pygame.sprite.Sprite):
    def __init__(self, i):
        super().__init__ 
        self.i = i 
        compare = body[self.i]
        self.x = compare.prevx
        self.y = compare.prevy
        self.prevx = self.x
        self.prevy = self.y
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.surf.fill(green)   
        
    def move(self):
        self.prevx = self.x
        self.prevy = self.y
        compare = body[self.i]
        self.x = compare.prevx
        self.y = compare.prevy
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size
        
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.x = 0
        self.y = 0
        self.surf = pygame.Surface((tile_size, tile_size))
        self.surf.fill(red)
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))
        self.move()
        
    def move(self):
               
        # create a rect for every tile
        move_sites = []
        for x in range(0, int(window_width/tile_size)):
            for y in range(margin, int(window_height/tile_size)):
                this = Rect((x * tile_size), (y * tile_size), tile_size, tile_size)
                move_sites.append(this)
                
        # remove every rect collidelisting with a member of body
       
        num_checked = 0
        move_to = []
        while num_checked < 480:
            #pygame.Rect.collidelist(tile, body) != -1
            if (pygame.Rect.collidelist(move_sites[num_checked], body) != -1):
                num_checked += 1
            else:
                move_to.append(move_sites[num_checked])
                num_checked += 1

        # choose a random one
        index = random.randint(0, len(move_to)-1)
        move_to_rect = move_to[index]
        self.rect = move_to_rect
        self.x = self.rect.x
        self.y = self.rect.y

Apple = Fruit()

def draw_grid(tile_size):
    # Draw vertical lines
    for x in range(0, window_width, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (x, margin*tile_size), (x, window_height))
    # Draw horizontal lines
    for y in range((margin*tile_size), window_height, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (0, y), (window_width, y))
    
movement_tick = 0
body_count = 0
high_score = 0

unpaused = True
# Game loop begin
while unpaused:
    
    # DO NOT DELETE THIS CODE
    # DELETING THIS CODE CAUSES THE GAME TO CRASH
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # close pygame window
            sys.exit()    # stop the python script
            
    # Draw the background
    DISPLAYSURF.blit(background_surf, background)
    
    # Draw grid
    draw_grid(50)
      
    # Draw the snake and body
    for entity in body:
        DISPLAYSURF.blit(entity.surf, entity.rect)
        
    # Draw the fruit
    DISPLAYSURF.blit(Apple.surf, Apple.rect)
    
    # Handle snake behaviour
    Snake.changeDirection()
    
    if (movement_tick == 5):
        movement_tick = 0
        for entity in body:
            entity.move()
    else:
        movement_tick += 1
      
    # if snake eats apple  
    if (pygame.Rect.colliderect(Snake.rect, Apple.rect)):
        new = Body(body_count)
        body.append(new)
        Apple.move()
        body_count += 1
        score += 1
            
    # if snake hits itself        
    if (pygame.Rect.collidelist(Snake.rect, body[1:]) != -1):
        Snake.kill
        Snake = Player()
        body = []
        body.append(Snake)
        body_count = 0
        if (score > high_score):
            high_score = score
        score = 0
    
    # Show score
    score_string = score_font.render(("Score: " + str(score)), True, white)
    high_score_text = high_score_font.render(("High Score: " + str(high_score)), True, white)
    DISPLAYSURF.blit(score_string, (30, 30))
    DISPLAYSURF.blit(high_score_text, (30, 120))
    
    pygame.display.update()
    FramePerSec.tick(FPS)