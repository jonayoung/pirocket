import pygame
import random
from pygame.locals import *
from math import *

# initialise pygame
pygame.init()
displayInfo = pygame.display.Info() # This var holds info about the screen, see http://www.pygame.org/docs/ref/display.html#pygame.display.Info
size = [displayInfo.current_w,displayInfo.current_h]  #Detect the width and height
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

WINFLAGS = pygame.FULLSCREEN                  # set to pygame.FULLSCREEN for full-screen
SCREENRECT = Rect(0, 0, displayInfo.current_w, displayInfo.current_h)     # the screen resolution
NSTARS = 1000
NASTEROIDS = 10
FPS = 30

# Initialize sprite groups
render = pygame.sprite.RenderUpdates()
 
# Colours in RGB space
# Each value is in the range 0-255
BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
TRANSPARENT = (1,2,3)
 
class Rocket(pygame.sprite.Sprite):
 
    colour = YELLOW
    thrust_value = 1.0
    turn_speed = 5
    max_speed = 10.0
 
    # draw base image
 
    #base_image = pygame.Surface((21, 11))
    base_image = pygame.image.load("rocket2.png").convert_alpha()
    #base_image.fill(TRANSPARENT)
    #base_image.set_colorkey(TRANSPARENT)
    #pointlist = [(0,0), (0,10), (20,5)]
    #pygame.draw.polygon(base_image, colour, pointlist)
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
               
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=SCREENRECT.center)
       
        self.vx = 0
        self.vy = 0
        self.angle = 0
        
        #self.bullets = pygame.sprite.RenderUpdates()
 
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        self.wrap()
 
    def wrap(self):
        if (self.rect.center[0] < 0):
            self.rect.move_ip(SCREENRECT.width, 0)           
        elif (self.rect.center[0] >= SCREENRECT.width):
            self.rect.move_ip(-SCREENRECT.width, 0)           
            
        if (self.rect.center[1] < 0):
           self.rect.move_ip(0, SCREENRECT.height)           
        elif (self.rect.center[1] >= SCREENRECT.height):
           self.rect.move_ip(0, -SCREENRECT.height)           
 
    def thrust(self):
        a = radians(self.angle)
        self.vx += self.thrust_value * cos(a)
        self.vy += self.thrust_value * sin(a)
 
        vel = sqrt(self.vx * self.vx + self.vy * self.vy)
        if (vel > self.max_speed):
            self.vx = self.vx * self.max_speed / vel
            self.vy = self.vy * self.max_speed / vel
 
    def turn(self, direction):
        self.angle += self.turn_speed * direction
        while (self.angle < 0):
            self.angle += 360
 
        while (self.angle >= 360):
            self.angle -= 360
 
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
 
    def fire(self):
        print("fire")
        tempBullet = Bullet(self.angle,self.rect.center[0],self.rect.center[1])
        render.add(tempBullet)

class Bullet(pygame.sprite.Sprite):
    base_image = pygame.Surface((50, 50))
    pygame.draw.circle(base_image, GREEN, (25,25), 5,0)

    def __init__(self,angle,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.base_image.copy()
        print("Bullet x:"+str(x))        
        self.rect = self.image.get_rect(center=(x,y))
        self.vx = 1
        self.vy = 1
    def update(self):
        self.rect.move_ip(self.vx, self.vy)        
            
class Asteroid(pygame.sprite.Sprite):
   
    min_speed = 2
    max_speed = 6
    base_image = pygame.image.load("roid.jpg").convert()
    #base_image = pygame.Surface((40, 50))
    #base_image.fill(TRANSPARENT)
    #base_image.set_colorkey(TRANSPARENT)
    #pointlist = [(10,0), (30,0), (40,15), (35,25), (20,50), (5,50), (0,25)]
    #pygame.draw.polygon(base_image, colour, pointlist)
   
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
               
        self.image = self.base_image.copy()
       
        x = int(SCREENRECT.width * random.random())
        y = int(SCREENRECT.height * random.random())       
        self.rect = self.image.get_rect(center=(x,y))
           
        velocity = random.randint(self.min_speed, self.max_speed)
        angle = 2.0 * pi * random.random() # radians
        self.vx = cos(angle) * velocity
        self.vy = sin(angle) * velocity    
     
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        self.wrap()
 
    def wrap(self):
        if (self.rect.center[0] < 0):
            self.rect.move_ip(SCREENRECT.width, 0)            
        elif (self.rect.center[0] >= SCREENRECT.width):
            self.rect.move_ip(-SCREENRECT.width, 0)           
            
        if (self.rect.center[1] < 0):
           self.rect.move_ip(0, SCREENRECT.height)           
        elif (self.rect.center[1] >= SCREENRECT.height):
           self.rect.move_ip(0, -SCREENRECT.height)           
 
def main():
 
    # Create a new window
    screen = pygame.display.set_mode(SCREENRECT.size, WINFLAGS)
 
    # Create a star map om the background  
    background = pygame.Surface(SCREENRECT.size)
    background.fill(BLACK)
    for i in range(0, NSTARS):
        x = random.randint(0, SCREENRECT.width-1)
        y = random.randint(0, SCREENRECT.height-1)
        pygame.draw.circle(background, WHITE, (x,y), 0)
   
    # copy the background onto the screen
    screen.blit(background, (0,0))
 
    # the screen is double buffered
    # changes will not appear until we update:
    pygame.display.update()
 
    # initialize our starting sprites
    rocket = Rocket()
 
    #Add rocket to render group
    render.add(rocket)
 
    # Create some asteroids
    asteroids = pygame.sprite.Group()
    for i in range(0,NASTEROIDS):
        # new asteroids are stored in the asteroids group
        asteroid = Asteroid()
        render.add(asteroid)
        asteroids.add(asteroid)
    clock = pygame.time.Clock()
 
    while True:
        # cap the framerate
        clock.tick(FPS)
 
        #get events   
        for event in pygame.event.get():
            if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
 
        # handle rocket actions
        keystate = pygame.key.get_pressed()
        if (keystate[K_UP]):
            rocket.thrust()
 
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        if (direction != 0):
            rocket.turn(direction)
 
        if (keystate[K_SPACE]):
            rocket.fire()
 
        # detect collisions
        for asteroid in pygame.sprite.spritecollide(rocket, asteroids, False):
            asteroid.kill()
 
        # update the sprites
        render.update()
        # draw the scene
        render.clear(screen, background)
        dirty = render.draw(screen)
        pygame.display.update(dirty)
 
# run main()
if __name__ == '__main__': main()