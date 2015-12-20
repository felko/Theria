#!/usr/bin/env python3
# coding: utf-8

import json

from sfml import sf

from .level import Level
from .entity.character.player import Player
from .types import *
from .constants import *


class Game:
	window = sf.RenderWindow(sf.VideoMode(*RESOLUTION),
							 'Theria',
							 sf.Style.DEFAULT)

	def __init__(self, level):
		self.level = level
		self.clock = sf.Clock()
		self.running = False

	@classmethod
	def load_from_file(cls, path):
		with open(path) as file:
			save = json.load(file)

			level = Level.load_json(save["level"])

			return cls(level)

	def update(self, dt):
		for event in self.window.events:

			if isinstance(event, sf.ResizeEvent):
				self.window.view.reset((0, 0, event.size.x, event.size.y))
				break
			elif isinstance(event, sf.CloseEvent):
				self.running = False
				break
			elif isinstance(event, sf.KeyEvent):
				if event.pressed:
					if event.code == sf.Keyboard.ESCAPE:
						self.running = False
						break
					elif event.code == sf.Keyboard.UP:
						self.level.player.move(Direction.up)
					elif event.code == sf.Keyboard.DOWN:
						self.level.player.move(Direction.down)
					elif event.code == sf.Keyboard.RIGHT:
						self.level.player.move(Direction.right)
					elif event.code == sf.Keyboard.LEFT:
						self.level.player.move(Direction.left)

			elif isinstance(event, sf.KeyEvent):
				if event.released:
					if event.code in (sf.Keyboard.UP,
									  sf.Keyboard.DOWN,
									  sf.Keyboard.RIGHT,
									  sf.Keyboard.LEFT):
						self.level.player.movement = Direction.null

		self.level.update(dt)

	def draw(self):
		self.window.clear()
		self.level.draw(self.window)
		self.window.display()

	def start(self):
		self.running = True

		while self.running:
			self.update(self.clock.restart())
			self.draw()