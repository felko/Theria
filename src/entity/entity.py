#!/usr/bin/env python3
# coding: utf-8

from sfml import sf

from ..types import *
from ..types.animation import *
from ..constants import *


class Entity:
	def __init__(self, pos, anim, texture_offset=Vec(0, 0)):
		self.position = pos
		self.animation = anim
		self.movement = Vec(0, 0)
		self.texture_offset = texture_offset
		self.time = sf.Time.ZERO

	def update(self, dt):
		self.time += dt

	def move(self, direction):
		self.movement = direction.value

	def get_anim_state(self):
		raise NotImplementedError('Class {!r} does not implement method'
						' get_anim_state'.format(self.__class__.__name__))

	def get_texture(self):
		state = self.get_anim_state()

		if isinstance(self.animation, Animation):
			return self.animation.get_frame(self.time)
		elif isinstance(self.animation, StateAnim):
			return self.animation.get_frame(state, self.time)

	def get_sprite(self):
		texture = self.get_texture()
		sprite = sf.Sprite(texture)
		sprite.position = self.position * TILE_SIZE
		return sprite

	def draw(self, target):
		sprite = self.get_sprite()
		target.draw(sprite)