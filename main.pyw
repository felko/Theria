#!/usr/bin/env python3
# coding: utf-8

from src.game import Game
from src.level import Level
from src.level.block import Block


def main():
	Block.load_files()
	level = Level.generate(16, 16)
	game = Game(level) #Game.load_from_file('saves/default.save')
	game.start()

if __name__ == '__main__':
	main()