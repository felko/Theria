#!/usr/bin/env python3
# coding: utf-8

from collections import namedtuple, OrderedDict
from enum import Enum

from ..parser import *
from ..types import *


class ObjectType(Enum):
	block = 1
	struct = 2


def named_tuple(cls, fields):
	@Parser
	def named_tuple_parser(string):
		match, rest = symbol('(').consume(string)
		result = dict()

		for field, parser in fields[:-1]:
			match, rest = symbol(field).consume(rest)
			match, rest = symbol(':').consume(rest)
			match, rest = lexeme(parser).consume(rest)
			result[field] = match
			match, rest = symbol(',').consume(rest)

		field, parser = fields[-1]
		match, rest = symbol(field).consume(rest)
		match, rest = symbol(':').consume(rest)
		match, rest = lexeme(parser).consume(rest)
		result[field] = match
		match, rest = symbol(')').consume(rest)

		return cls(**result), rest

	return named_tuple_parser


size_instr = namedtuple('size', ['width', 'height'])
fill_instr = namedtuple('fill', ['rect', 'element'])

pos = named_tuple(Vec, [('x', integer), ('y', integer)])
rect = named_tuple(Rect, [('x', integer), ('y', integer), ('w', integer), ('h', integer)])

size = symbol('size') > named_tuple(size_instr, [('width', integer), ('height', integer)])
fill = symbol('rect') >

format = size &

#from src.region.loader import *
# size.parse('size (width: 64, height: 32)')