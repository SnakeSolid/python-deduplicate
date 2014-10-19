#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


class Deduplicator:
	def __init__(self, files, min_size):
		self.files = files
		self.min_size = min_size
	
	def process(self):
		pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create hardlinks for similar files in directory.')
	parser.add_argument("-s", "--min-size", type=int, default="1024", help='minimal file size to check (bytes)')
	parser.add_argument('files', metavar='file', type=str, nargs='+', help='list of files or directories')

	args = parser.parse_args()
	
	deduplicator = Deduplicator(args.files, args.min_size)
	deduplicator.process()