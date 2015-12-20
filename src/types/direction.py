#!/usr/bin/env python3
# coding: utf-8

from enum import Enum

from .vec import *


class Direction(Vec, Enum):
	def __hash__(self):
		return hash(self.value)

	up = 0, -1
	down = 0, 1
	right = 1, 0
	left = -1, 0
	null = 0, 0