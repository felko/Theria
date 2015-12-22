#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

from .types import *


class Movement:
	"""
	Linear interpolation movement between two given positions.
	"""

	def __init__(self, vec, duration=sf.Time.ZERO):
		if duration == sf.Time.ZERO:
			self.speed = Vec(*vec)
			self.duration = sf.Time()
			self.duration.microseconds = 1
		else:
			self.speed = Vec(*vec) / duration.seconds
			self.duration = duration

	def __repr__(self):
		return '<Movement {} ending in {}>'.format(self.speed, self.duration)

	@classmethod
	def link(cls, start, dest, duration=sf.Time.ZERO):
		"""
		Creates a Movement object from two points.

		:param start: The starting position
		:param dest: The destination
		:param duration: The duration of the movement
		:return: A Movement object
		"""

		delta = Vec(*dest) - Vec(*start)
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

		if self.duration:
			self.duration = max(self.duration - dt, sf.Time.ZERO)
			pos += self.speed * self.duration.seconds

	def terminate(self):
		"""
		Stop the movement.
		"""

		self.duration = sf.Time.ZERO
		self.speed = Vec(0, 0)

	def copy(self):
		mov = Movement(Vec(0, 0))
		mov.speed = self.speed
		mov.duration = self.duration
		return mov


idle = Movement((0, 0))