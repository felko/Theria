#!/usr/bin/env python3
# coding: utf-8

import itertools

import numpy as np

from ..block import Block
from ..tile import Tile
from ...types import *


class Biome(np.ndarray):
	def __new__(cls, width, height):
		reg = super().__new__(cls, (width, height), dtype=Tile)
		reg.width, reg.height = width, height
		reg.fill(Block.registered['air'])
		return reg

	@classmethod
	def generate(cls, width, height):
		return cls(width, height)

	@staticmethod
	def load_json(data):
		width = data['width']
		height = data['height']
		biome_type_name = data['type']
		reg = get_biome(biome_type_name)(width, height)

		tiles = data['tiles']

		if len(tiles) != height:
			raise ValueError('Specified height ({}) does not match given tiles'
							 .format(height))

		for y, row in enumerate(tiles):
			if len(row) != width:
				raise ValueError('Specified width ({}) does not match the {}{}'
								 ' row'.format(height, y,
								 'st' if y == 1 else 'nd' if y == 2 else 'th'))

			for x, block_data in enumerate(row):
				reg[x, y] = Tile(Vec(x, y), Block.load_json(block_data))

		return reg

	def fill(self, block):
		coords = itertools.product(range(self.width), range(self.height))

		for pos in coords:
			self[pos] = Tile(pos, block)


def get_biome(name):
	for biome in Biome.__subclasses__():
		if biome.__name__ == name:
			return biome

	return Biome