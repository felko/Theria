#!/usr/bin/env python3
# coding: utf-8

import os
import glob
import json

from sfml import sf

from ..action import Action
import src.action as action
from ..constants import *


class Block:
	registered = dict()

	def __init__(self, ID=None, solid=False, texture=TEXTURE_UNKNOWN, register=True):
		self.ID = ID
		self.solid = solid
		self.texture = texture
		self.on_enter = action.nothing
		self.on_exit = action.nothing
		self.on_action = action.nothing
		self.on_stumble = action.nothing

		if register:
			if ID:
				Block.register(self)
			else:
				raise ValueError('Expected ID to be other than None')

	def __repr__(self):
		return '<Block {!r}>'.format(self.ID)

	@classmethod
	def register(cls, block):
		cls.registered[block.ID] = block

	@staticmethod
	def load_files(paths='src/assets/blocks'):
		if isinstance(paths, str):
			pattern = os.path.join(paths, '*.block')
			for block_data_path in glob.iglob(pattern):
				with open(block_data_path) as file:
					data = json.load(file)
					Block(ID=os.path.basename(block_data_path).split('.')[0],
						  solid=data['solid'],
						  texture=sf.Texture.from_file(data['texture']))
		else:
			for path in paths:
				Block.load_files(path)


	@classmethod
	def load_json(cls, data):
		if isinstance(data, str):
			return cls.registered[data]
		elif isinstance(data, dict):
			if 'ID' in data:
				block = cls.registered[data['ID']]
			else:
				solid = data['solid']
				texture = sf.Texture.from_file(data['texture'])
				block = cls(solid, texture, register=False)

			action = data.get('action', None)

			if action is not None:
				block.on_enter = Action.load_json(action['on_enter'])
				block.on_exit = Action.load_json(action['on_exit'])
				block.on_action = Action.load_json(action['on_action'])
				block.on_stumble = Action.load_json(action['on_stumble'])

			return block