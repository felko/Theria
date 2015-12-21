#!/usr/bin/env python3
# coding: utf-8

import os
import glob

from sfml import sf


class Animation:
	"""
	An animated texture.
	"""

	def __init__(self, frames, interval=sf.Time.ZERO):
		"""
		:param frames: Iterable of sf.Texture objects
		:param interval: Time between two frames (default: 0.0s)
		"""

		self.frames = frames
		self.interval = interval
		self.index = 0
		self.time = sf.Time.ZERO

	@classmethod
	def load_from_dir(cls, path, interval=None):
		"""
		Load an animation from a directory. Directory must contain some image
		files named by their index (e.g. "1.png", "2.png", etc...)

		:param path: str object, path to the directory to load
		:param interval: Time between two frames
		:return: Animation
		"""

		if path[-1] not in (os.sep, '/'):
			path += os.sep

		frames = list()
		for frame_path in glob.iglob(path + '[0-9].png'):
			frame = sf.Texture.from_file(frame_path)
			frames.append(frame)

		if interval is not None:
			return cls(frames)
		else:
			return cls(frames, interval)

	def get_frame(self, dt):
		"""
		Returns the texture of the entity.

		:param dt: The time between the current and the previous frame.
		:return: A sf.Texture instance
		"""

		self.time += dt

		if self.time > self.interval:
			self.time = sf.Time.ZERO
			self.index += 1
			self.index %= len(self.frames)

		return self.frames[self.index]

