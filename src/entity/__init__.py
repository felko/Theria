#!/usr/bin/env python3
# coding: utf-8

from ..types import *
from ..constants import *


class Entity:
	def __init__(self, pos):
		self.pos = pos

	@property
	def rect(self):
		return Rect(self.pos, Vec(TILE_SIZE, TILE_SIZE))