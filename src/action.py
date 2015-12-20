#!/usr/bin/env python3
# coding: utf-8


class Action:
	registered = dict()

	def __init__(self, fn, register=True):
		self.fn = fn

		if register:
			Action.registered[fn.__name__] = self

	def __call__(self, entity):
		return self.fn(entity)

	@classmethod
	def load_json(cls, data):
		if isinstance(data, str):
			return cls.registered[data]
		else:
			raise TypeError('JSON field action should be a string')

	@classmethod
	def anonymous(cls, fn):
		return cls(fn, register=False)


@Action
def nothing(entity):
	pass


def debug(message):
	@Action.anonymous
	def wrapper(entity):
		nonlocal message
		print(message)

	return wrapper