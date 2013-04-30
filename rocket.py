#Import the whole of the pygame lib
import pygame
from pygame.locals import *

from random import randint  #import randint, to allow us to generate some randomness later

# Define some colors  - We might use these later
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)


# Define the rocket class
class rocket:
  def __init__(self):
    self.speed = 10 #How big the steps of the rocket are (effectively speed)
    self.posX = 0  #Where the rocket is on the X axis
    self.posY = 0  #Where the rocket is on the Y axis
    self.velocityX = 0 #If 0 the rocket is still, otherwise it will move by this much next blip
    self.velocityY = 0 #If 0 the rocket is still, otherwise it will move by this much next blip
    self.image = pygame.image.load("rocket.png").convert() #The picture of the rocket!
    self.image.set_colorkey(white) #Removes the white background
    self.width = self.image.get_width()
    self.height = self.image.get_height()
#Finished defining the rocket class  


#Define the astroid class
class asteroid(pygame.sprite.Sprite):
  base_image = pygame.Surface((100,92)) # Set surface the same size as the image below.
  
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.speed = 1 # Speed not yet used - might need to be done differently, Do we need an angle...?
    self.x = 200 #X position
    self.y = 200 #Y position
    self.image = pygame.image.load("roid.jpg").convert() #The picture of the asteroid
    self.rect = self.image.get_rect(center=(self.x,self.y)) #The rectangle, sets the starting position of the roid
  
  #def update(self):
    #Will be used to move the roid
    
#Setup the Game
 
pygame.init()
  
# Set Game to be full screen
displayInfo = pygame.display.Info() # This var holds info about the screen, see http://www.pygame.org/docs/ref/display.html#pygame.display.Info
size = [displayInfo.current_w,displayInfo.current_h]  #Detect the width and height
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
screenSizeX = displayInfo.current_w  #Set the same variables as before for use later
screenSizeY = displayInfo.current_h
 
#Loop until the user clicks the close button.
done = False

#If true will print out debug messages
debug = True
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Instantiate the rocket class
rocket = rocket()
#Set the rocket to start in the middle
rocket.posX = screenSizeX/2
rocket.posY = screenSizeY/2


#Create an sprite group to hold the astroids, see - http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
asteroids = pygame.sprite.Group()

#Add a starting asteroid
roid1 = asteroid()
asteroids.add(roid1)
#Here we need a loop to populate the sprite group 

if debug:
    print("Rocket Width:"+str(rocket.width))
    print("Rocket Height:"+str(rocket.height))
# -------- Main Program Loop -----------
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
          done = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN: #A Key was pressed down
          print("User pressed a key.")
          if event.key == K_ESCAPE: #If the escape key is pressed exit the game
            done = True 
          if event.key == K_UP: #Test for Up arrow
            rocket.velocityY = -rocket.speed # minus as we need to move up the screen
          if event.key == K_DOWN: #Test for Down arrow
            rocket.velocityY = rocket.speed
          if event.key == K_RIGHT:
            rocket.velocityX = rocket.speed
          if event.key == K_LEFT:
            rocket.velocityX = -rocket.speed # minus to move left
        if event.type == pygame.KEYUP: # A Key was released
          if event.key == K_UP:
            rocket.velocityY = 0 
          if event.key == K_DOWN:
            rocket.velocityY = 0
          if event.key == K_RIGHT:
            rocket.velocityX = 0
          if event.key == K_LEFT:
            rocket.velocityX = 0
            
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    
    #Check the left hand border
    if (rocket.posX + rocket.velocityX) <= 0:
        rocket.posX = screenSizeX - rocket.width
    else:
        #Move the rocket X
        rocket.posX = rocket.posX + rocket.velocityX
        
    #Check the right hand border    
    if (rocket.posX + rocket.velocityX) >= screenSizeX:
        rocket.posX = 0 + rocket.width
    else:
        rocket.posX = rocket.posX + rocket.velocityX
    
    #Check the top
    if (rocket.posY + rocket.velocityY) <= 0:
        print("Hit the top")
        rocket.posY = screenSizeY - rocket.height
    else:
        #Move the rocket Y
        rocket.posY = rocket.posY + rocket.velocityY
        
    #Check the bottom
    if (rocket.posY + rocket.velocityY) >= screenSizeY:
        rocket.posY = 0 + rocket.height
    else:
        #Move the rocket Y
        rocket.posY = rocket.posY + rocket.velocityY        
        
    if debug: 
      print('Rocket X Position:' + str(rocket.posX))
      print('Rocket Y Position:' + str(rocket.posY))
      
    asteroids.update() # Move the roids?
    
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    
    asteroids.draw(screen) #Draw all the roids onto the screen, this method not explicitly defined as part of the Sprite class.
    
    screen.blit(rocket.image, [rocket.posX,rocket.posY]) #Draw the rocket onto the screen

     
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(20)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()