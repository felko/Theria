#!/usr/bin/env python3
# coding: utf-8

import itertools

from sfml import sf

from .region import Region
from .entity.character.player import Player
from .types import *


class Level:
	def __init__(self, region, player, entities=()):
		self.region = region
		self.player = player
		self.entities = list(entities)

	@classmethod
	def load_json(cls, data):
		region = Region.load_from_file(data['region'])
		player = Player.load_json(data['player'])
		return cls(region, player)

	def update(self, dt):
		self.player.update(dt)
		self.move(self.player)

		for entity in self.entities:
			entity.update(dt)
			self.move(entity)

	def move(self, entity):
		if not self.region[tuple(entity.position + entity.movement)].block.solid:
			entity.position += entity.movement

		entity.movement = Vec(0, 0)

	def draw(self, target):
		coords = itertools.product(range(self.region.width), range(self.region.height))

		for x, y in coords:
			tile = self.region[x, y]
			target.draw(tile.get_sprite())

		self.player.draw(target)

		for entity in self.entities:
			entity.draw(target)