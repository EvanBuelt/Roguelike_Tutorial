import libtcodpy as libtcod
import pygame

# game files
import constants

SURFACE_MAIN = None
GAME_MAP = None


# Struct
class StructTile:
    def __init__(self, block_path):
        self.block_path = block_path


# Map
def map_create():
    new_map = [[StructTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


# Drawing
def draw_game():

    global SURFACE_MAIN, GAME_MAP

    # clear the screen
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200, 200))

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path is True:
                # Draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            else:
                # Draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


# Game
def game_main_loop():
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

    global SURFACE_MAIN, GAME_MAP

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    GAME_MAP = map_create()


# Execute game
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
