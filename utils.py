import pygame, os, random, math, json
from constants import *


BASE_PATH = './assets/'

# =====================================================
# ============ MISC HELPER FUNCTIONS ==================
# =====================================================
def load_image(path):
    img : pygame.Surface = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_dir(path) :
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        if img_name == ".DS_Store" :
            continue
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
        # ** Instance variable
        self.tile_assets = {}
        for key in tiles :
            self.tile_assets[key] = load_image(tiles[key])
    # ========= LOAD GENERAL ASSETS =========
        assets = world["assets"]
        # ** Instance variable
        self.assets = {}
        for key in assets :
            if key == "animations" :
                continue
            self.assets[key] = load_image(assets[key])
    # ========= LOAD ANIMATIONS =========
        animations = assets["animations"]
        # ** Instance variable
        self.animations = {}
        for key in animations :
            self.animations[key] = load_dir(animations[key])
    # ========= HANDLE MAP =========
    # the absence of a coordinate in "map" in the json indicates that it's just a blank tile
    # NOTE : tile_map dict will have raw tuples as keys, while json will have strings of tuples as keys
        # ** Instance variable
        self.tile_map = {}
        for y in range(TILES_DOWN) :
            for x in range(TILES_ACROSS) :
                # DEFAULT VALUE POPULATION
                if stringFromTuple((x, y)) not in world["map"].keys():
                    self.tile_map[(x, y)] = 0
                
        self.mode = 0

# =====================================================
# ============ ENTITY CLASS ===========================
# =====================================================
class Entity :
    def __init__(self, box : pygame.Rect, sprite : pygame.Surface, state : dict ) -> None:
        self.box            = box
        self.sprite         = sprite
        self.state          = state