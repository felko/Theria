#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

RESOLUTION = 1024, 512
TILE_SIZE = 16

TEXTURE_UNKNOWN = sf.Texture.from_file('src/assets/textures/blocks/unknown.png')


def sign(x):
	if x < 0:
		return -1
	elif x == 0:
		return 0
	elif x > 0:
		return 1