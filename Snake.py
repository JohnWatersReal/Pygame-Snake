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
white = pygame.Color(255, 255, 255)

# Display Setup
DISPLAYSURF = pygame.display.set_mode((window_width,window_height))
background = Rect(0, 0, window_width, window_height)
background_surf = pygame.Surface((window_width, window_height))
background_surf.fill(black)

# Setting Framerate
FPS = 12
FramePerSec = pygame.time.Clock()

# Setting window title
pygame.display.set_caption("Game")

# Setting up fonts
score_font = pygame.font.SysFont("Comic_sans", 60)
high_score_font = pygame.font.SysFont("Comic_sans", 30, False, True)

# Setting up pause screen
pause_rect = Rect(window_width/3, window_height/3, window_width/3, window_height/3)

# Setting up grid
tile_size = 50
margin = 4

# Snake object list
body = []   

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.x = 2
        self.y = 4
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = self.surf.get_rect(topleft=(self.x*tile_size, self.y*tile_size))
        self.surf.fill(green)
        self.dx = 1
        self.dy = 0
        
    def move(self):
        new = Body(self.x, self.y)
        body.append(new)
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size
        
        # going over or under the vertical limits
        if self.rect.y >= window_height:
            self.rect.y = margin*tile_size
            self.y = margin
        if self.rect.y < margin*tile_size:
            self.rect.y = window_height - tile_size
            self.y = window_height/tile_size - 1
        # going over or under the horizonal limits
        if self.rect.right > window_width:
            self.rect.x = 0
            self.x = 0
        if self.rect.left < 0:
            self.rect.x = window_width - tile_size
            self.x = window_width/tile_size - 1
            
    def change_direction_flag(self, key):
        if self.dx == 0:
            if key == K_RIGHT:
                self.flag = 0
            elif key == K_LEFT:
                self.flag = 1
        elif self.dy == 0:
            if key == K_DOWN:
                self.flag = 2
            elif key == K_UP:
                self.flag = 3       
            
    def change_direction(self):
            if self.flag == 0:
                self.dx = 1
                self.dy = 0
            elif self.flag == 1:
                self.dx = -1
                self.dy = 0
     
            elif self.flag == 2:
                self.dx = 0
                self.dy = 1
            elif self.flag == 3:
                self.dx = 0
                self.dy = -1
         
class Tail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.x = 0
        self.y = 4
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.surf.fill(green)  
        
    def move(self):
        compare = body[2]
        self.x = compare.x
        self.y = compare.y
        self.rect = Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        del body[2]
        
        
class Body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__ 
        self.x = x
        self.y = y
        self.surf = pygame.Surface((tile_size, tile_size))
        self.rect = Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.surf.fill(green)   
        
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
            if pygame.Rect.collidelist(move_sites[num_checked], body) != -1:
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

def draw_grid(tile_size):
    # Draw vertical lines
    for x in range(0, window_width, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (x, margin*tile_size), (x, window_height))
    # Draw horizontal lines
    for y in range((margin*tile_size), window_height, tile_size):
        pygame.draw.line(DISPLAYSURF, grey, (0, y), (window_width, y))
    
def pause_check(paused):
    while (paused):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() # close pygame window
                sys.exit()    # stop the python script
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False 
   
# Global variables 
snake = Player() 
body.append(snake)
apple = Fruit()
tail = Tail()
tail_move = True
body.append(tail)
starting_body = Body(1, 4)
body.append(starting_body)
score = 0
high_score = 0
unpaused = True
# Game loop begin
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # close pygame window
            sys.exit()    # stop the python script
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.draw.rect(DISPLAYSURF, white, pause_rect)
                paused = score_font.render("PAUSED", True, black)
                rect = paused.get_rect(center=(window_width/2, window_height/2))
                DISPLAYSURF.blit(paused, rect)
                pygame.display.update()
                pause_check(True)
            else: 
                snake.change_direction_flag(event.key)
            
    # Draw the background
    DISPLAYSURF.blit(background_surf, background)
    
    # Draw grid
    draw_grid(tile_size)
      
    # Draw the snake and body
    for entity in body:
        DISPLAYSURF.blit(entity.surf, entity.rect)
        
    # Draw the fruit
    DISPLAYSURF.blit(apple.surf, apple.rect)
    
    # Handle snake movement
    snake.change_direction()
    snake.move()
    if tail_move:
            tail.move()
    tail_move = True
      
    # if snake eats apple  
    if pygame.Rect.colliderect(snake.rect, apple.rect):
        tail_move = False
        apple.move()
        score += 1 
    
    # if snake hits itself
    if pygame.Rect.collidelist(snake.rect, body[1:]) != -1:
        del(snake)
        snake = Player()
        del(tail)
        tail = Tail()
        new = Body(1, 4)
        body = []
        body.extend([snake, tail, new])
        if score > high_score:
            high_score = score
        score = 0
        
    # Show score
    score_string = score_font.render(("Score: " + str(score)), True, white)
    DISPLAYSURF.blit(score_string, (30, 30))
    high_score_text = high_score_font.render(("High Score: " + str(high_score)), True, white)
    DISPLAYSURF.blit(high_score_text, (30, 120))
    
    pygame.display.update()
    FramePerSec.tick(FPS)
    