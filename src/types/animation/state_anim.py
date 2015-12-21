#!/usr/bin/env python3
# coding: utf-8

__all__ = ['StateAnim']

import os
from sfml import sf

from .animation import Animation
from ...helper import flatten_dict


class StateAnim:
	"""
	A state-dependent animated texture.
	"""

	def __init__(self, frame_mapping, default=None):
		"""
		:param frame_mapping: Dictionary mapping a state to an Animation or to
			a sf.Texture object
		"""

		self.frame_mapping = frame_mapping
		self.state = default

	@classmethod
	def load_from_dir(cls, path, default=None):
		"""
		Loads a MultiAnimation object from a directory.

		For example, the following directory tree:
			+- walking
			|---+ right
			|   |--- 0.png
			|   |--- 1.png
			|   |--- 2.png
			|---+ left
			|   |--- 0.png
			|   |--- 1.png
			|   |--- 2.png
			+- running
			|---+ right
			|   |--- 0.png
			|   |--- 1.png
			|   |--- 2.png
			|---+ left
			|   |--- 0.png
			|   |--- 1.png
			|   |--- 2.png
		... is interpreted as a mapping of a (movement, direction) tuple to an
		animation.

		:param path: str object, path to the directory to load
		:return: MultiAnimation object
		"""

		nested_mapping = _load_mapping(path)
		flattened_mapping = flatten_dict(nested_mapping)

		return cls(flattened_mapping, default)

	def get_frame(self, state, dt):
		"""
		Return the frame at a given state and time.

		:param state: The state of the entity
		:param dt: The time between the current and the previous frame
		:return: A sf.Texture object
		"""

		if state == self.state:
			anim = self.frame_mapping[state]
			if isinstance(anim, Animation):
				return anim.get_frame(dt)
			else:
				return anim
		else:
			self.state = state


def _load_mapping(path):
	"""
	Recursive helper function for class method StateAnim.load_from_dir.

	:param path:
	:return:
	"""

	mapping = dict()

	for sub in os.listdir(path):
		state_name = os.path.basename(sub)
		sub_path = os.path.join(path, sub)

		if os.path.isdir(sub_path):
			if any(os.path.isdir(os.path.join(sub_path, d)) for d in os.listdir(sub_path)):
				mapping[state_name] = _load_mapping(sub_path)
			elif all(name.split('.')[0].isdigit() for name in map(os.path.basename, os.listdir(sub_path))):
				mapping[state_name] = Animation.load_from_dir(sub_path)
			else:
				mapping[state_name] = _load_mapping(sub_path)
		else:
			mapping[state_name.split('.')[0]] = sf.Texture.from_file(sub_path)

	return mapping