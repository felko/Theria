#!/usr/bin/env python3
# coding: utf-8

from functools import wraps


class Action:
	registered = dict()

	def __init__(self, fn):
		self.fn = fn

	def __repr__(self):
		return '<Action {!r}>'.format(self.fn.__name__)

	def __call__(self, entity):
		return self.fn(entity)

	@classmethod
	def load_json(cls, data):
		if isinstance(data, str):
			return cls.registered[data]
		else:
			raise TypeError('JSON field action should be a string')

	@classmethod
	def register(cls, fn):
		"""
		Instantiate a new Action and register it.

		:param fn: The underlying Python callable object
		:return: The registered Action instance
		"""

		if isinstance(fn, Action):
			action = fn
			cls.registered[action.fn.__name__] = action
		else:
			action = cls(fn)
			cls.registered[fn.__name__] = action

		return action

	@classmethod
	def parametrized(cls, fn):
		"""
		Instantiates a parametrized action.

		:param fn: The underlying Python callable object
		:return: Python function returning an Action instance
		"""

		@wraps(fn)
		def wrapper(*args, **kwds):
			action = fn(*args, **kwds)
			return Action(action)

		return wrapper


@Action.register
def nothing(entity):
	pass


@Action.register
@Action.parametrized
def debug(message):
	def wrapper(entity):
		print(message)

	return wrapper
