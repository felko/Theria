#!/usr/bin/env python3
# coding: utf-8

import time
import json

from .level import Level
from .types import *
from .constants import *


class Game:

	def __init__(self, level):
		self.level = level
		self.clock = sf.Clock()
		self.running = False
		self.pressed_keys = set()
		self.window = sf.RenderWindow(
			sf.VideoMode(*RESOLUTION),
			'Theria',
			sf.Style.DEFAULT
		)
		self.view = sf.View()
		self.view.size = RESOLUTION
		self.view.center = self.level.player.rect.center * TILE_SIZE
		self.window.view = self.view

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

	def handle_events(self):
		for event in self.window.events:

			if isinstance(event, sf.ResizeEvent):
				self.window.view.reset((0, 0, event.size.x, event.size.y))
			elif isinstance(event, sf.CloseEvent):
				self.running = False
				break
			elif isinstance(event, sf.KeyEvent):
				if event.pressed:
					self.pressed_keys.add(event.code)
				elif event.released and event.code in self.pressed_keys:
					self.pressed_keys.remove(event.code)

	def update(self, dt):
		"""
		Performs action depending on the user input and updates the level.

		:param dt: Time between the current and the previous frame
		"""

		self.handle_events()

		if sf.Keyboard.UP in self.pressed_keys:
			self.level.player.move(Direction.up)
		elif sf.Keyboard.DOWN in self.pressed_keys:
			self.level.player.move(Direction.down)
		elif sf.Keyboard.RIGHT in self.pressed_keys:
			self.level.player.move(Direction.right)
		elif sf.Keyboard.LEFT in self.pressed_keys:
			self.level.player.move(Direction.left)

		self.level.update(dt)
		self.view.center = self.level.player.rect.center * TILE_SIZE

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