#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

RESOLUTION = 1024, 512
TILE_SIZE = 16

TEXTURE_UNKNOWN = sf.Texture.from_file('src/assets/textures/blocks/unknown.png')

ENTITY_MOVE_DURATION = .2
PLAYER_ANIM_INTERVAL = ENTITY_MOVE_DURATION / 3

BIOME_SIZE = 16, 16