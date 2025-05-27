import pygame, sys, random
from pygame.locals import *

pygame.init()

# Window Settings
window_width = 1500
window_height = 1000

# Creating Colours
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
grey = pygame.Color(128, 128, 128)
blue = pygame.Color(0, 0, 255)

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
font = pygame.font.SysFont("Comic_sans", 60)

tile_size = 50

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.x = 0
        self.y = 0
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))
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
        
        if (self.rect.y >= window_height):
            self.rect.y = 0
            self.y = 0
        if (self.rect.y < 0):
            self.rect.y = window_height
            self.y = window_height/tile_size 
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
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size
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
        self.x = random.randint(0, int(window_width/tile_size) - 1)
        self.y = random.randint(0, int(window_height/tile_size) - 1)
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size
           

# Create player object

Apple = Fruit()

def draw_grid(tile_size):
    for x in range(tile_size, window_width, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (x, 0), (x, window_height))
    for y in range(tile_size, window_height, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (0, y), (window_width, y))
    
movement_tick = 0
body_count = 0
body_group = pygame.sprite.Group()


# Game loop begin
while True:
    
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
      
    #if snake eats apple  
    if (pygame.Rect.colliderect(Snake.rect, Apple.rect)):
        Apple.move()
        new = Body(body_count)
        body.append(new)
        body_count += 1
        score += 1
            
    # if snake hits itself        
    if (pygame.Rect.collidelist(Snake.rect, body[1:]) != -1):
        pygame.quit()
        sys.exit()
    
    # Show score
    score_string = font.render(("Score: " + str(score)), True, blue)
    DISPLAYSURF.blit(score_string, (30, 30))
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)