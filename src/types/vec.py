#!/usr/bin/env python3
# coding: utf-8

from math import sqrt, log10
from sfml import sf

from ..constants import *


class Vec:
	"""
	Two dimensional vector.
	"""

	__slots__ = ['x', 'y']

	def __init__(self, x, y):
		self.x, self.y = x, y

	def __repr__(self):
		return 'Vec(x={}, y={})'.format(*self)

	@classmethod
	def link(cls, a, b):
		return Vec(b.x - a.x, b.y - a.y)

	def __add__(self, other):
		dx, dy = other
		return Vec(self.x + dx, self.y + dy)

	def __sub__(self, other):
		dx, dy = other
		return Vec(self.x - dx, self.y - dy)

	def __mul__(self, other):
		if isinstance(other, (Vec, tuple)):
			kx, ky = other
			return Vec(self.x * kx, self.y * ky)
		else:
			return Vec(self.x * other, self.y * other)

	def __truediv__(self, other):
		if isinstance(other, (Vec, tuple)):
			kx, ky = other
			return Vec(self.x / kx, self.y / ky)
		else:
			return Vec(self.x / other, self.y / other)

	def __floordiv__(self, other):
		if isinstance(other, (Vec, tuple)):
			x, y = other
			return Vec(self.x // x, self.y // y)
		else:
			return Vec(self.x // other, self.y // other)

	def __neg__(self):
		return Vec(-self.x, -self.y)

	def __bool__(self):
		return self.x == 0 and self.y == 0

	def __iter__(self):
		return iter((self.x, self.y))

	def __hash__(self):
		return hash((self.x, self.y))

	@property
	def norm(self):
		return sqrt(self.x ** 2 + self.y ** 2)

	@norm.setter
	def norm(self, value):
		self.x, self.y = self.unit * value

	@property
	def tile(self):
		return self // TILE_SIZE

	@tile.setter
	def tile(self, value):
		self.x, self.y = value * TILE_SIZE

	@property
	def unit(self):
		return self // int(self.norm)

	@unit.setter
	def unit(self, value):
		self.x, self.y = value.unit * self.norm