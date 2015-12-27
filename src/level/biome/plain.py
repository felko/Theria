#!/usr/bin/env python3
# coding: utf-8

import random
import itertools

from .biome import Biome
from ..block import Block
from ..tile import Tile


class Plain(Biome):
	@classmethod
	def generate(cls, width, height):
		biome = cls(width, height)
		biome.fill(Block.registered['grass'])

		coords = itertools.product(range(biome.width), range(biome.height))
		n = random.randrange(biome.width * biome.height // 2)

		for pos in random.sample(list(coords), n):
			biome[pos] = Tile(pos, Block.registered['flower'])

		return biome