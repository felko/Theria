#!/usr/bin/env python3
# coding: utf-8

from ..entity import Entity
from ...types import *


class Character(Entity):
	def __init__(self, pos, anim, texture_offset=Vec(0, 0)):
		super().__init__(pos, anim, texture_offset)
		self.facing = Direction.down

	def move(self, direction):
		if not self.movement:
			self.facing = direction

		super().move(direction)