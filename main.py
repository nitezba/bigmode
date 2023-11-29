import pygame, sys, random, math, wave, os, json
from pygame.locals import *
from utils import *
from constants import *

clock = pygame.time.Clock()

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
# every 10 seconds
pygame.time.set_timer(TIMER_EVENT, 10000)
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
        if event.type == TIMER_EVENT :
            world.mode = not world.mode

    # ------------ key held down event polling ------------
    keys = pygame.key.get_pressed()

    # ============ STATE HANDLING ============

    # ============ RENDERING ============
    for coord in world.tile_map.keys() :
        if world.mode == 0 : # ** dark mode
            if world.tile_map[coord] == 0 :
                raw_window.blit(world.tile_assets['dark base tile'], (TILE_SIZE * coord[0], TILE_SIZE * coord[1]))
        elif world.mode == 1 : # ** dark mode
            if world.tile_map[coord] == 0 :
                raw_window.blit(world.tile_assets['light base tile'], (TILE_SIZE * coord[0], TILE_SIZE * coord[1]))
            
    
    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()

    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)