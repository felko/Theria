#!/usr/bin/env python3
# coding: utf-8

import itertools
import json

from ..entity.character.player import Player
from .biome import *
from ..types import *


class Level:
	def __init__(self, region, player, entities=()):
		self.region = region
		self.player = player
		self.entities = list(entities)

	@classmethod
	def load_json(cls, data):
		"""
		Loads a JSON-formatted object to a Level.

		:param data: dictionary
		:return: The loaded Level object.
		"""

		with open(data['region']['file']) as level_file:
			level_data = json.load(level_file)

		reg_x, reg_y = data['region']['biome_x'], data['region']['biome_y']
		region_data = level_data[reg_y][reg_x]

		region = Biome.load_json(region_data)
		player = Player.load_json(data['player'])
		return cls(region, player)

	@classmethod
	def generate(cls, width, height):
		reg = Plain.generate(width, height)

		pos = (random.randrange(reg.width), random.randrange(reg.height))
		while reg[pos].block.solid:
			pos = (random.randrange(reg.width), random.randrange(reg.height))

		player = Player(pos)
		lvl = cls(reg, player)

		return lvl

	def update(self, dt):
		"""
		Updates each entity given the time between the current and the previous
		frame.

		:param dt: Time between the current and the previous frame
		"""

		self.player.update(dt)
		self.move(self.player, dt)

		for entity in self.entities:
			entity.update(dt)
			self.move(entity, dt)

	def move(self, entity, dt):
		"""
		Apply to each entity their movement, taking account of collisions.

		:param entity: The Entity instance to move
		:param dt: The seconds between the current and the previous frame
		"""

		new_pos = entity.movement.apply(entity.position, dt)

		try:
			if self.region[tuple(entity.movement.end_pos)].block.solid:
				entity.movement.terminate()
			else:
				entity.position = new_pos
		except IndexError:
			pass

	def draw(self, target):
		"""
		Draws the level and the entities to the given render window.

		:param target: sf.RenderWindow to draw on
		"""

		coords = itertools.product(range(self.region.width), range(self.region.height))

		for x, y in coords:
			tile = self.region[x, y]
			target.draw(tile.get_sprite())

		self.player.draw(target)

		for entity in self.entities:
			entity.draw(target)