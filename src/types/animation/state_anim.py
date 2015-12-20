#!/usr/bin/env python3
# coding: utf-8

import os
from sfml import sf

from .animation import Animation


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

		def load_mapping(path):
			mapping = dict()

			for sub in os.listdir(path):
				state_name = os.path.basename(sub)
				sub_path = os.path.join(path, sub)

				if os.path.isdir(sub_path):
					if any(os.path.isdir(os.path.join(sub_path, d)) for d in os.listdir(sub_path)):
						mapping[state_name] = load_mapping(sub_path)
					elif all(name.split('.')[0].isdigit() for name in map(os.path.basename, os.listdir(sub_path))):
						mapping[state_name] = Animation.load_from_dir(sub_path)
					else:
						mapping[state_name] = load_mapping(sub_path)
				else:
					mapping[state_name.split('.')[0]] = sf.Texture.from_file(sub_path)

			return mapping

		def flatten_dict(dct):
			flattened = dict()

			for k, v in dct.items():
				if isinstance(v, dict):
					sub_dct = flatten_dict(v)
					for subk, subv in sub_dct.items():
						if isinstance(subk, tuple):
							flattened[(k,) + subk] = subv
						else:
							flattened[k, subk] = subv
				else:
					flattened[k] = v

			return flattened

		nested_mapping = load_mapping(path)
		flattened_mapping = flatten_dict(nested_mapping)

		return cls(flattened_mapping, default)

	def get_frame(self, state, dt):
		if state == self.state:
			anim = self.frame_mapping[state]
			if isinstance(anim, Animation):
				return anim.get_frame(dt)
			else:
				return anim
		else:
			self.state = state