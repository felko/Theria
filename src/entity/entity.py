#!/usr/bin/env python3
# coding: utf-8

from ..movement import *
from ..types import *
from ..animation import *
from ..constants import *


class Entity:
	def __init__(self, pos, anim, texture_offset=Vec(0, 0)):
		self.position = pos
		self.animation = anim
		self.movement = idle
		self.texture_offset = texture_offset
		self.dt = 0

		if isinstance(anim, StateAnim):
			self.animation.state = self.get_anim_state()

	@property
	def rect(self):
		return Rect(self.position, (1, 1))

	def update(self, dt):
		"""
		Updates the entity's clock.

		:param dt: Time between the current and the previous frame.
		"""

		self.dt = dt

	def move(self, direction):
		"""
		Performs an orthogonal movement on the entity.

		:param direction: A Direction object.
		"""

		if not self.movement:
			self.movement = Movement(direction.value, ENTITY_MOVE_DURATION)

	def get_anim_state(self):
		"""
		Returnsthe current state of the entity.
		"""

		raise NotImplementedError('Class {!r} does not implement method'
		                          ' get_anim_state'.format(self.__class__.__name__))

	def get_texture(self):
		"""
		Return the current texture of the entity.

		:return: A sf.Texture object
		"""

		if isinstance(self.animation, sf.Texture):
			return self.animation
		else:
			state = self.get_anim_state()

			if isinstance(self.animation, Animation):
				return self.animation.get_frame(self.dt)
			elif isinstance(self.animation, StateAnim):
				return self.animation.get_frame(state, self.dt)

	def get_sprite(self):
		"""
		Return the sprite of the entity, with the right position in pixels and
		the current texture.

		:return: A sf.Sprite object
		"""

		texture = self.get_texture()
		sprite = sf.Sprite(texture)
		sprite.position = self.position * TILE_SIZE
		return sprite

	def draw(self, target):
		"""
		Draw the entity to the given render window

		:param target: The sf.RenderWindow object to draw on
		"""

		sprite = self.get_sprite()
		target.draw(sprite)