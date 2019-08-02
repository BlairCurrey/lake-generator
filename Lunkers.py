import pygame

pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
bgd_image = pygame.image.load("map.png")


#Border variables - this should probably be a class!
#Also, perhaps "dirty rectangles" is the solution to making this functional
#take square around boat, save, then blit to the border window
pip_width = int(width / 4)
pip_height = int(height / 4)
pip_border_thickness = 3
pip_border_color = (0,0,0)
pip_x = width - pip_width - 25
pip_y = height - pip_height - 25
pip_image = pygame.transform.scale(bgd_image, (pip_width, pip_height))

#Another class - boat
boat_image = pygame.image.load("boat.png")
x_pos = pip_x / 2 
y_pos = height / 2 

# define a main function
def main():
     
    # create a surface on screen that has the size of 1280 x 720
    screen = pygame.display.set_mode(size)

    # blits map
    screen.blit(bgd_image, (0,0))

    #blits boat
    screen.blit(boat_image, (x_pos, y_pos))

    #blits picture-in-picture with black border
    screen.blit(pip_image, (pip_x, pip_y))
    
    #BORDER
    #top line
    pygame.draw.rect(screen, pip_border_color, [pip_x, pip_y - pip_border_thickness, pip_width, pip_border_thickness])
    # bottom line
    pygame.draw.rect(screen, pip_border_color, [pip_x,pip_y + pip_height, pip_width, pip_border_thickness])
    # left line
    pygame.draw.rect(screen, pip_border_color, [pip_x - pip_border_thickness, pip_y - pip_border_thickness, pip_border_thickness, pip_height + 2 * pip_border_thickness])
    # right line
    pygame.draw.rect(screen, pip_border_color, [pip_x + pip_width, pip_y - pip_border_thickness, pip_border_thickness, pip_height + 2 * pip_border_thickness])

	#updates screen    
    pygame.display.flip()
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()