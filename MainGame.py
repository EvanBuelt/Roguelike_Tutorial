import libtcodpy as libtcod
import pygame

# ASCII Art: http://patorjk.com/software/taag/#p=display&f=Big&t=Type%20Something%20

#   _____                        ______ _ _
#  / ____|                      |  ____(_) |
# | |  __  __ _ _ __ ___   ___  | |__   _| | ___  ___
# | | |_ |/ _` | '_ ` _ \ / _ \ |  __| | | |/ _ \/ __|
# | |__| | (_| | | | | | |  __/ | |    | | |  __/\__ \
#  \_____|\__,_|_| |_| |_|\___| |_|    |_|_|\___||___/
import constants

SURFACE_MAIN = None
GAME_MAP = None
PLAYER = None
ENEMY = None
GAME_OBJECTS = None


#   _____ _                   _
#  / ____| |                 | |
# | (___ | |_ _ __ _   _  ___| |_
#  \___ \| __| '__| | | |/ __| __|
#  ____) | |_| |  | |_| | (__| |_
# |_____/ \__|_|   \__,_|\___|\__|

class StructTile:
    def __init__(self, block_path):
        self.block_path = block_path


#   ____  _     _           _
#  / __ \| |   (_)         | |
# | |  | | |__  _  ___  ___| |_ ___
# | |  | | '_ \| |/ _ \/ __| __/ __|
# | |__| | |_) | |  __/ (__| |_\__ \
#  \____/|_.__/| |\___|\___|\__|___/
#             _/ |
#            |__/

class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # Map Address
        self.y = y  # Map Address
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        global SURFACE_MAIN
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):
        global GAME_OBJECTS
        tile_is_wall = GAME_MAP[self.x + dx][self.y + dy].block_path

        target = None

        for object in GAME_OBJECTS:
            if (object is not self and
                    object.x == self.x + dx and
                    object.y == self.y + dy and
                    object.creature):
                target = object
                break

        if target:
            print self.creature.name_instance + " attacks " + target.creature.name_instance

        if not tile_is_wall:
            self.x += dx
            self.y += dy


#   _____                                             _
#  / ____|                                           | |
# | |     ___  _ __ ___  _ __   ___  _ __   ___ _ __ | |_ ___
# | |    / _ \| '_ ` _ \| '_ \ / _ \| '_ \ / _ \ '_ \| __/ __|
# | |___| (_) | | | | | | |_) | (_) | | | |  __/ | | | |_\__ \
#  \_____\___/|_| |_| |_| .__/ \___/|_| |_|\___|_| |_|\__|___/
#                       | |
#                       |_|

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


#           _____
#     /\   |_   _|
#    /  \    | |
#   / /\ \   | |
#  / ____ \ _| |_
# /_/    \_\_____|

class AITest:
    """
    Once per turn, execute
    """
    def take_turn(self):
        self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))


#  __  __
# |  \/  |
# | \  / | __ _ _ __
# | |\/| |/ _` | '_ \
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/
#              | |
#              |_|

def map_create():
    new_map = [[StructTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(0, constants.MAP_HEIGHT):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    for y in range(0, constants.MAP_WIDTH):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

    return new_map


#  _____                     _
# |  __ \                   (_)
# | |  | |_ __ __ ___      ___ _ __   __ _
# | |  | | '__/ _` \ \ /\ / / | '_ \ / _` |
# | |__| | | | (_| |\ V  V /| | | | | (_| |
# |_____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                     __/ |
#                                    |___/

def draw_game():

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # clear the screen
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    for obj in GAME_OBJECTS:
        obj.draw()

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


#   _____
#  / ____|
# | |  __  __ _ _ __ ___   ___
# | | |_ |/ _` | '_ ` _ \ / _ \
# | |__| | (_| | | | | | |  __/
#  \_____|\__,_|_| |_| |_|\___|

def game_main_loop():
    """
    In this function, we loop the main game
    """

    global GAME_OBJECTS

    player_action = "No Action"

    game_quit = False
    while not game_quit:
        # Player action definition
        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True

        elif player_action != "No Action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initialize():
    """
    This function initializes the main window and pygame
    """

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))
    GAME_MAP = map_create()

    creature_com1 = ComCreature("Greg")
    PLAYER = ObjActor(1, 1, "Python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("Bobby")
    ai_com = AITest()
    ENEMY = ObjActor(15, 15, "Crab", constants.S_ENEMY, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]


def game_handle_keys():
    game_quit = False

    # Get Player Input
    event_list = pygame.event.get()

    # Process Input
    for event in event_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.move(0, -1)
                return "Player Moved"
            elif event.key == pygame.K_DOWN:
                PLAYER.move(0, 1)
                return "Player Moved"
            elif event.key == pygame.K_LEFT:
                PLAYER.move(-1, 0)
                return "Player Moved"
            elif event.key == pygame.K_RIGHT:
                PLAYER.move(1, 0)
                return "Player Moved"

    return "No Action"


#  ______                     _          _____
# |  ____|                   | |        / ____|
# | |__  __  _____  ___ _   _| |_ ___  | |  __  __ _ _ __ ___   ___
# |  __| \ \/ / _ \/ __| | | | __/ _ \ | | |_ |/ _` | '_ ` _ \ / _ \
# | |____ >  <  __/ (__| |_| | ||  __/ | |__| | (_| | | | | | |  __/
# |______/_/\_\___|\___|\__,_|\__\___|  \_____|\__,_|_| |_| |_|\___|

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
