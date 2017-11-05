import libtcodpy as libtcod
import pygame

# game files
import constants

SURFACE_MAIN = None
GAME_MAP = None
PLAYER = None
ENEMY = None


# Struct
class StructTile:
    def __init__(self, block_path):
        self.block_path = block_path


# Objects
class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature=None):
        self.x = x  # Map Address
        self.y = y  # Map Address
        self.sprite = sprite

        if creature:
            self.creature = creature
            creature.owner = self

    def draw(self):
        global SURFACE_MAIN
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy


# Components
class ComCreature:
    '''
    Creatures have health, can damage other objects by attacking them, and can also die.
    '''
    def __init__(self, name_instance, hp=10):
        self.name_instance = name_instance
        self.hp = hp


class ComItem:
    def __init__(self):
        return


class ComContainer:
    def __init__(self):
        return


# Map
def map_create():
    new_map = [[StructTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


# Drawing
def draw_game():

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY

    # clear the screen
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    ENEMY.draw()
    PLAYER.draw()

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initialize():
    '''This function initializes the main window and pygame'''

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    GAME_MAP = map_create()

    creature_com1 = ComCreature("Greg")
    PLAYER = ObjActor(0, 0, "Python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("Bobby")
    ENEMY = ObjActor(15, 15, "Crab", constants.S_ENEMY, creature=creature_com2)


# Execute game
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
