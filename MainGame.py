import libtcodpy as libtcod
import pygame

# game files
import constants

SURFACE_MAIN = None


def draw_game():

    global SURFACE_MAIN

    # clear the screen
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # TODO: draw the map

    # draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200, 200))

    # update the display
    pygame.display.flip()

def main_loop():
    '''In this function, we loop the main game'''

    game_quit = False
    a = 0
    while not game_quit:

        # Get Player Input
        event_list = pygame.event.get()

        # Process Input
        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initialize():
    '''This function initializes the main window and pygame'''

    global SURFACE_MAIN

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))


if __name__ == '__main__':
    game_initialize()
    main_loop()
