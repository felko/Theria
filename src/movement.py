#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

from .helper import time
from .types import *


class Movement:
	"""
	Linear interpolation movement between two given positions.
	"""

	def __init__(self, vec, duration=time(seconds=1)):
		if duration == sf.Time.ZERO:
			self.duration = time(seconds=1)

		self.speed = Vec(*vec) / duration.milliseconds
		self.duration = duration

	def __repr__(self):
		return '<Movement {} ending in {}>'.format(self.speed, self.duration)

	@classmethod
	def link(cls, start, dest, duration=None):
		"""
		Creates a Movement object from two points.

		:param start: The starting position
		:param dest: The destination
		:param duration: The duration of the movement
		:return: A Movement object
		"""

		delta = Vec(*dest) - Vec(*start)

		if duration is None:
			return cls(delta)
		else:
			return cls(delta, duration)

	def __bool__(self):
		return bool(self.speed)

	def apply(self, pos, dt):
		"""
		Time-dependent movement of the given position. Returns the remaining
		movement to achieve to finish the movement.

		:param pos: The position to move
		:param dt: The time between the current and the previous frame
		"""

		pos.x, pos.y = pos + self.speed * self.duration.milliseconds
		self.duration = max(self.duration - dt, sf.Time.ZERO)

	def terminate(self):
		"""
		Stop the movement.
		"""

		self.duration = sf.Time.ZERO
		self.speed = Vec(0, 0)

	def copy(self):
		mov = Movement(Vec(0, 0))
		mov.speed = self.speed.copy()
		mov.duration = self.duration
		return mov


idle = Movement((0, 0))