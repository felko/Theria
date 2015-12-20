#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

from .animation import Animation
from .state_anim import StateAnim
from .. import *
from ...constants import *


class AnimatedSprite:
	def __init__(self, position, animation, texture_offset=Vec(0, 0)):
		"""
		:param pos: Position of the Sprite
		:param anim: Animation
		"""

		self.position = position
		self.animation = animation
		self.movement = Direction.null

		if isinstance(animation, StateAnim):
			self.animation.current_state = self.get_anim_state()

		self.anim_iter = self.get_animation_iterable(animation)
		self.texture_offset = texture_offset

	@property
	def rect(self):
		return Rect(self.pos, Vec(1, 1))

	def get_anim_state(self):
		raise NotImplementedError('Method get_anim_state is not implemented'
			' for class {!r}'.format(self.__class__))

	def draw(self, target):
		sprite = sf.Sprite(next(self.anim_iter))
		sprite.position = self.position * TILE_SIZE + self.texture_offset
		target.draw(sprite)