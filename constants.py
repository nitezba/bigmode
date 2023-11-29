import pygame, os, random, math, json

mapFile = open('data.json')
data = json.load(mapFile)
mapFile.close()

TILE_SIZE = 16

TILES_ACROSS = 42
TILES_DOWN = 26

WINDOW_WIDTH = TILE_SIZE * TILES_ACROSS
WINDOW_HEIGHT = TILE_SIZE * TILES_DOWN

TIMER_EVENT = pygame.event.custom_type()