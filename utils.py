import pygame, os, random, math, json

BASE_PATH = './assets/'

# =====================================================
# ============ MISC HELPER FUNCTIONS ==================
# =====================================================
def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_dir(path) :
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def stringFromTuple (t : tuple) -> str:
    ret = "("
    for elt in t :
        ret += str(elt) + ","
    ret = ret[:-1]
    ret += ")"
    return ret

# =====================================================
# ============ WORLD CLASS ============================
# =====================================================
class World() :
    def __init__(self) -> None:
        # ========= OPEN FILE =========
        mapFile = open('data.json')
        data = json.load(mapFile)
        mapFile.close()
        world = data["world"]
        # ========= LOAD TILE ASSETS =========
        tiles = world["tile_assets"]
        self.tile_assets = {}
        for key in tiles :
            self.tile_assets[key] = load_image(tiles[key])
        # ========= LOAD GENERAL ASSETS =========
        assets = world["assets"]
        self.assets = {}
        for key in assets :
            self.assets[key] = load_image(assets[key])
        # ========= HANDLE MAP =========
        # the absence of a coordinate in "map" in the json indicates that it's just a blank tile
        # NOTE : tile_map dict will have raw tuples as keys, while json will have strings of tuples as keys
        self.tile_map = {}
        for y in range(world["window_data"]["tiles_down"]) :
            for x in range(world["window_data"]["tiles_across"]) :
                # DEFAULT VALUE POPULATION
                if stringFromTuple((x, y)) not in world["map"].keys():
                    self.tile_map[(x, y)] = 0
                
        self.level_number = 0

# =====================================================
# ============ ENTITY CLASS ===========================
# =====================================================
class Entity :
    def __init__(self, box : pygame.Rect, sprite : pygame.Surface, state : dict ) -> None:
        self.box            = box
        self.sprite         = sprite
        self.state          = state