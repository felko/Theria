#!/usr/bin/env python3
# coding: utf-8

from .vec import *


class Rect:
	"""
	Rectangle in 2D space.
	"""

	def __init__(self, *args, **kwds):
		if len(args) == 4:
			self.x, self.y, self.w, self.h = args
		elif len(args) == 2:
			pos, size = args
			self.x, self.y = pos
			self.w, self.h = size
		elif len(args) == 0:
			if len(kwds) == 4:
				self.x, self.y = kwds['x'], kwds['y']
				self.w, self.h = kwds['w'], kwds['h']
			elif len(kwds) == 2:
				self.x, self.y = kwds['pos']
				self.w, self.h = kwds['size']
			else:
				raise ValueError('Not enough keyword arguments')
		else:
			raise ValueError('Not enough positional arguments')


	@classmethod
	def link(cls, a, b):
		return Vec(a, b - a)

	@property
	def pos(self):
		return Vec(self.x, self.y)

	@pos.setter
	def pos(self, value):
		self.x, self.y = value

	@property
	def size(self):
		return Vec(self.w, self.h)

	@size.setter
	def size(self, value):
		self.w, self.h = value

	@property
	def topleft(self):
		return self.pos

	@topleft.setter
	def topleft(self, value):
		self.pos = value

	@property
	def topright(self):
		return Vec(self.x + self.w, self.y)

	@topright.setter
	def topright(self, value):
		x, y = value
		self.x, self.y = x - self.w, self.y

	@property
	def bottomleft(self):
		return Vec(self.x, self.y + self.h)

	@bottomleft.setter
	def bottomleft(self, value):
		x, y = value
		self.x, self.y = x, y - self.h

	@property
	def bottomright(self):
		return Vec(self.x + self.w, self.y + self.h)

	@bottomright.setter
	def bottomright(self, value):
		x, y = value
		self.x, self.y = x - self.w, y - self.h

	@property
	def center(self):
	    return self.pos + Vec.link(self.topleft, self.bottomright) / 2

	@center.setter
	def center(self, value):
		x, y = value
		self.x, self.y = value - Vec.link(self.topleft, self.bottomright) / 2