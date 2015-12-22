#!/usr/bin/env python3
# coding: utf-8

from enum import Enum

from .character import Character
from ...types.animation.state_anim import StateAnim
from .. import *

PLAYER_ANIM = StateAnim.load_from_dir('src/assets/sprites/player')


class Player(Character):
	def __init__(self, pos):
		super().__init__(pos, PLAYER_ANIM, Vec(0, -3))

	@classmethod
	def load_json(cls, data):
		pos = Vec(data['x'], data['y'])
		return cls(pos)

	def get_anim_state(self):
		if self.movement:
			print(self.movement)
			return PlayerMovement.walking.name, self.facing.name
		else:
			return PlayerMovement.idle.name, self.facing.name


class PlayerMovement(Enum):
	idle = 0
	walking = 1