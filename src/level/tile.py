#!/usr/bin/env python3
# coding: utf-8

import sfml as sf

from ..types import *
from ..constants import *


class Tile:
	def __init__(self, position, block):
		self.position = Vec(*position)
		self.block = block

	def __repr__(self):
		return '<Tile {} {!r}>'.format(self.position, self.block.ID)

	def get_sprite(self):
		sprite = sf.Sprite(self.block.texture)
		sprite.position = tuple(self.position * TILE_SIZE)
		return sprite