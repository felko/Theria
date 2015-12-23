#!/usr/bin/env python3
# coding: utf-8

from src.game import Game
from src.region.block import Block


def main():
	Block.load_files()
	game = Game.load_from_file('saves/default.save')
	game.start()

if __name__ == '__main__':
	main()