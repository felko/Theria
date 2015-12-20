#!/usr/bin/env python3
# coding: utf-8

import itertools
import numpy as np
import json

from src.region.block import Block
from src.region.tile import Tile

from ..types import *
from ..constants import *


class Region(np.ndarray):
	def __new__(cls, width, height):
		reg = super().__new__(cls, (width, height), dtype=Tile)

		coords = itertools.product(range(width), range(height))

		for pos in coords:
			reg[pos] = Tile(pos, Block.registered['air'])

		return reg

	def __init__(self, width, height):
		self.width, self.height = width, height

	@classmethod
	def load_from_file(cls, path):
		with open(path) as file:
			data = json.load(file)
			return cls.load_json(data)

	@classmethod
	def load_json(cls, data):
		width = data['width']
		height = data['height']
		reg = cls(width, height)

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

	@property
	def size(self):
		return self.width, self.height

	@size.setter
	def size(self, value):
		self.reshape(value)