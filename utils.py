import pygame, os, random, math, json

from constants import *
from helper_structures import *


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
    # ============================ init function ============================
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

    # ============================ get neighbors function ============================
    def getTileNeighbors(self, coord: tuple) -> dict :
        tiles = {
            "top" : {},
            "middle" : {},
            "bottom" : {}
        }
        
        tiles["top"]["left"] = (coord[0] - 1, coord[1] - 1) if coord[0] > 0 and coord[1] > 0 else None
        tiles["top"]["middle"] = (coord[0], coord[1] - 1) if coord[1] > 0 else None
        tiles["top"]["right"] = (coord[0] + 1, coord[1] - 1) if coord[0] < WINDOW_WIDTH / TILE_SIZE - 1 and coord[1] > 0 else None
       
        tiles["middle"]["left"] = (coord[0] - 1, coord[1]) if coord[0] > 0  else None
        tiles["middle"]["middle"] = None
        tiles["middle"]["right"] = (coord[0] + 1, coord[1]) if coord[0] < WINDOW_WIDTH / TILE_SIZE - 1 else None

        tiles["bottom"]["left"] = (coord[0] - 1, coord[1] + 1) if coord[0] > 0 and coord[1] < WINDOW_HEIGHT / TILE_SIZE - 1 else None
        tiles["bottom"]["middle"] = (coord[0], coord[1] + 1) if coord[1] < WINDOW_HEIGHT / TILE_SIZE - 10 else None
        tiles["bottom"]["right"] = (coord[0] + 1, coord[1] + 1) if coord[0] < WINDOW_WIDTH / TILE_SIZE - 1 and coord[1] < WINDOW_HEIGHT / TILE_SIZE - 1 else None
         
        return tiles
    
    # ============================ binary space partition function ============================
    def spacePartition(self, root : partitionCell) -> Tree: 
        tree = []
        leaves = []
        frontier = []
        frontier.append(root)

        # ------------- tree creation -------------
        while frontier:
            node : partitionCell = frontier[0]
            frontier.remove(frontier[0])
            if node.isDonePartitioning() :
                leaves.append(node)
                tree.append(node)
                continue

            orientation = 1 if random.random() >= .5 else 0
            # extract middle two quarters of space
            space = node.getVerticalRange() if orientation == 1 else node.getHorizontalRange()
            # TODO: expose to json 
            space_size = abs(space[0] - space[1])
            middle = (space[0] + math.floor(space_size / 4), space[1] - math.floor(space_size / 4))
            spliceLocation = random.randrange(middle[0], middle[1])
            
            # TODO: CHECK IF THIS WORKS LMFAO
            # split up cell into children 
            # partitionCell(topLeft, bottomRight, parent)
            node.split(orientation, spliceLocation)
            
            tree.append(node)

            frontier.append(node.children[0])
            frontier.append(node.children[1])

        # ------------- post processing -------------
        skinnies : list = []
        for node in leaves:
            dims : tuple = node.getDimensions()
            if dims[0] <= 2 or dims [1] <= 2:
                skinnies.append(node)

        for node in skinnies :
            parent = node.parent
            for child in parent.children:
                if child in leaves:
                    leaves.remove(child)
            tree.remove(parent)
            parent.children = None
            leaves.append(parent)

        final_tree = Tree(tree, leaves)
        return final_tree
    
    # ============================ cellular automata function ============================
    def cellularAutomata(self, area : partitionCell, asset_place : int = 1, asset_ignore : int = 0, spawn_chance : int = .5) :
        num_iterations = 2
        neighbor_requirement = 4

        # for key in self.tile_map.keys() :
        for key in area.getInternalCoords() :
            place_tile = 1 if random.random() <= spawn_chance else 0

            if place_tile :
                # rocks.append(key)
                self.tile_map[key] = asset_place

        to_remove   : list  = []
        to_add      : list  = []

        for i in range(num_iterations):
            for key in area.getInternalCoords() :
                neighbors = self.getTileNeighbors(key)
                count = 0
                for row in neighbors.keys():
                    for col in neighbors[row].keys() :
                        neighbor_coord = neighbors[row][col]
                        
                        if neighbor_coord != None:
                            if self.tile_map[neighbor_coord] == asset_place :
                                count += 1
                if count >= neighbor_requirement :
                    to_add.append(key)
                else :
                    to_remove.append(key)

            for coord in to_add :
                self.tile_map[coord] = asset_place

            for coord in to_remove :
                self.tile_map[coord] = asset_ignore
                
# =====================================================
# ============ ENTITY CLASS ===========================
# =====================================================
class Entity :
    def __init__(self, box : pygame.Rect, sprite : pygame.Surface, state : dict ) -> None:
        self.box            = box
        self.sprite         = sprite
        self.state          = state

    