#!/usr/bin/env python3
# coding: utf-8

from ..entity import Entity
from ...types import *


class Character(Entity):
	def __init__(self, pos, anim, texture_offset=Vec(0, 0)):
		self.facing = Direction.down
		super().__init__(pos, anim, texture_offset)

	def move(self, direction):
		if not self.movement:
			self.facing = direction

		super().move(direction)