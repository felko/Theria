#!/usr/bin/env python3
# coding: utf-8

import re


class ParseError(Exception):
	pass


class Parser:
	def __init__(self, fn, trans=lambda x: x):
		self._function = fn
		self.trans = trans

	def __and__(self, other):
		@Parser
		def _chain_parser(string):
			match1, rest1 = self.consume(string)
			match2, rest2 = other.consume(rest1)
			return (match1, match2), rest2

		_chain_parser.name = '(' + self.name + ') then (' + other.name + ')'

		return _chain_parser

	def __or__(self, other):
		@Parser
		def _alternative_parser(string):
			try:
				return self.consume(string)
			except ParseError:
				return other.consume(string)

		_alternative_parser.name = '(' + self.name + ') or (' + other.name + ')'

		return _alternative_parser

	def __lt__(self, other):
		@Parser
		def _chain_parser(string):
			match1, rest1 = self.consume(string)
			match2, rest2 = other.consume(rest1)
			return match1, rest2

		_chain_parser.name = '(' + self.name + ') followed by (' + other.name + ')'

		return _chain_parser

	def __gt__(self, other):
		@Parser
		def _chain_parser(string):
			match1, rest1 = self.consume(string)
			match2, rest2 = other.consume(rest1)
			return match2, rest2

		_chain_parser.name = '(' + other.name + ') following (' + self.name + ')'

		return _chain_parser

	def __rshift__(self, trans):
		def new_trans(x):
			return trans(self.trans(x))

		return Parser(self._function, new_trans)

	def __rlshift__(self, trans):
		def new_trans(x):
			return trans(self.trans(x))

		return Parser(self._function, new_trans)

	@property
	def name(self):
		return self._function.__name__

	@name.setter
	def name(self, value):
		self._function.__name__ = value

	def consume(self, string):
		match, rest = self._function(string)
		return self.trans(match), rest

	def parse(self, string):
		match, rest = self.consume(string)

		if rest:
			raise ParseError('Unable to match the whole string, remaining {!r}'.format(rest))

		return match


def satisfy(predicate):
	@Parser
	def satisfy_parser(string):
		if not string:
			raise ParseError('Empty string')

		fst, rest = string[0], string[1:]

		if predicate(fst):
			return fst, rest
		else:
			raise ParseError('Unable to match predicate {0.__name__!r} to character {1!r}'.format(predicate, fst))

	satisfy_parser.name = "satisfy " + predicate.__name__

	return satisfy_parser


def many(parser):
	@Parser
	def many_parser(string):
		result = list()
		rest = string

		try:
			while rest:
				match, rest = parser.consume(rest)
				result.append(match)
		except ParseError:
			pass
		finally:
			return result, rest

	many_parser.name = "many " + parser.name

	return many_parser


def some(parser):
	@Parser
	def some_parser(string):
		result = list()

		match, rest = parser.consume(string)
		result.append(match)

		try:
			while rest:
				match, rest = parser.consume(rest)
				result.append(match)
		except ParseError:
			pass
		finally:
			return result, rest

	some_parser.name = 'some (' + parser.name + ')'

	return some_parser


def string(s):
	@Parser
	def string_parser(string):
		if string.startswith(s):
			return s, string[len(s):]
		else:
			raise ParseError('Unable to match prefix {!r} to string {!r}'.format(s, string))

	return string_parser


def between(begin, end):

	def between_combinator(parser):
		return begin > (parser < end)

	return between_combinator


def sep_by(sep):
	def sep_combinator(parser):
		@Parser
		def _sep_parser(string):
			result = list()
			rest = string

			try:
				while rest:
					match, rest = (parser < sep).consume(rest)
					result.append(match)
			except ParseError:
				match, rest = parser.consume(rest)
				result.append(match)
			finally:
				return result, rest

		_sep_parser.name = '(' + parser.name + ') separated by (' + sep.name + ')'

		return _sep_parser

	return sep_combinator


def sep_by1(sep):
	def sep_combinator(parser):
		@Parser
		def _sep_parser(string):
			result = list()

			match, rest = (parser < sep).consume(string)
			result.append(match)

			try:
				while rest:
					match, rest = (parser < sep).consume(rest)
					result.append(match)
			except ParseError:
				match, rest = parser.consume(rest)
				result.append(match)
			finally:
				return result, rest

		_sep_parser.name = '(' + parser.name + ') separated by (' + sep.name + ')'

		return _sep_parser

	return sep_combinator


def regex(pattern):
	@Parser
	def regex_parser(string):
		match = re.match(pattern, string)

		if match is not None:
			rest = string[match.end():]
			return match, rest
		else:
			raise ParseError('Unable to match regular expression {!r} to string {!r}'.format(pattern, string))

	return regex_parser


space = satisfy(str.isspace)
spaces = many(space)
letter = satisfy(str.isalpha)
lexeme = lambda parser: parser < spaces
symbol = lambda sym: lexeme(string(sym))

parens = between(string('('), string(')'))
brackets = between(string('['), string(']'))
braces = between(string('{'), string('}'))

digit = satisfy(str.isdigit)
integer = some(digit) >> ''.join >> int
float = ((integer < string('.')) & integer) >> (lambda x: map(str, x)) >> '.'.join >> float
number = float | integer