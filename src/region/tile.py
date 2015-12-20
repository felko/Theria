#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

from ..types import *
from ..constants import *


class Tile:
	def __init__(self, position, block):
		self.position = position
		self.block = block

	def __repr__(self):
		return '<Tile {} {!r}>'.format(self.position, self.block.ID)

	def get_sprite(self):
		sprite = sf.Sprite(self.block.texture)
		sprite.position = self.position * TILE_SIZE
		return sprite