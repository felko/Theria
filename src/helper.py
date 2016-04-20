#!/usr/bin/env python3
# coding: utf-8

import sfml as sf


def sign(x):
	if x < 0:
		return -1
	elif x == 0:
		return 0
	elif x > 0:
		return 1


def flatten_dict(dct):
	flattened = dict()

	for k, v in dct.items():
		if isinstance(v, dict):
			sub_dct = flatten_dict(v)
			for subk, subv in sub_dct.items():
				if isinstance(subk, tuple):
					flattened[(k,) + subk] = subv
				else:
					flattened[k, subk] = subv
		else:
			flattened[k] = v

	return flattened


def time(seconds=0, milliseconds=0):
	t = sf.Time()
	t.milliseconds = milliseconds + seconds * 1000
	return t