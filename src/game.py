#!/usr/bin/env python3
# coding: utf-8

import time
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
		"""
		Load a game from a *.save file.

		:param path: The path to the save file
		:return: The loaded Game instance
		"""

		with open(path) as file:
			save = json.load(file)

			level = Level.load_json(save["level"])

			return cls(level)

	def update(self, dt):
		"""
		Performs action depending on the user input and updates the level.

		:param dt: Time between the current and the previous frame
		"""

		for event in self.window.events:

			if isinstance(event, sf.ResizeEvent):
				self.window.view.reset((0, 0, event.size.x, event.size.y))
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

		self.level.update(dt)

	def draw(self):
		self.window.clear()
		self.level.draw(self.window)
		self.window.display()

	def start(self):
		self.running = True
		t = time.time()

		while self.running:
			dt = time.time() - t
			t = time.time()
			self.update(dt)
			self.draw()