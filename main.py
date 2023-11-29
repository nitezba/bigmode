import pygame, sys, random, math, wave, os, json
clock = pygame.time.Clock()

# NOTE - could be made more flexible by specifying top down or side scrolling

from pygame.locals import *
from utils import *

mapFile = open('data.json')
data = json.load(mapFile)
mapFile.close()
TILE_SIZE = data["world"]["tile_data"]["size"]

WINDOW_WIDTH = TILE_SIZE * data["world"]["window_data"]["tiles_across"]
WINDOW_HEIGHT = TILE_SIZE * data["world"]["window_data"]["tiles_down"]

pygame.init() 

display_window = pygame.display.set_mode((WINDOW_WIDTH * 2, WINDOW_HEIGHT * 2), 0, 32)
raw_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

# =====================================================
# ============ DATA DECLARATION =======================
# =====================================================
playing = True
world = World()

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start
# =====================================================
# ============ MAIN GAME LOOP =========================
# =====================================================
while playing :
    frame_start = frame_end
    raw_window.fill((0,0,0))

    # ============ EVENT HANDLING ============
    # ------------ single keypress event polling ------------
    for event in pygame.event.get() :
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: 
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # ------------ key held down event polling ------------
    keys = pygame.key.get_pressed()

    # ============ STATE HANDLING ============

    # ============ RENDERING ============
    for coord in world.tile_map.keys() :
        if world.tile_map[coord] == 0 :
            raw_window.blit(world.tile_assets['base tile'], (TILE_SIZE * coord[0], TILE_SIZE * coord[1]))
    
    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()