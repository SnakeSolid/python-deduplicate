#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import collections
import hashlib
import os


class Deduplicator:
	BLOCK_SIZE = 4096
	
	def __init__(self, files, min_size):
		self.files = files
		self.min_size = min_size
	
	def walk(self, path, append):
		if os.path.isfile(path):
			append(path)
		elif os.path.isdir(path):
			for listed in os.listdir(path):
				self.walk(os.path.join(path, listed), append)
	
	def fingerprint(self, path):
		with open(path) as reader:
			hasher_md5 = hashlib.md5()
			hasher_sha256 = hashlib.sha256()
			
			while True:
				data_buffer = reader.read(self.BLOCK_SIZE)

				if len(data_buffer) == 0:
					break
				
				hasher_md5.update(data_buffer)
				hasher_sha256.update(data_buffer)
				
			return { "path": path, "size": os.path.getsize(path), "md5": hasher_md5.hexdigest(), "sha256": hasher_sha256.hexdigest() }
		return None
	
	def create_symlinks(self, path_list):
		source_path = path_list[0]
		
		for destination_path in path_list[1:]:
			os.remove(destination_path)
			os.link(source_path, destination_path)
	
	def process(self):
		all_files = []
		
		for path in self.files:
			self.walk(os.path.expanduser(path), all_files.append)
		
		choosen_files = (listed for listed in all_files if os.path.getsize(listed) > self.min_size)
		hashed_files = (self.fingerprint(listed) for listed in choosen_files)
		collected_files = collections.defaultdict(list)
		
		for listed in hashed_files:
			path = listed["path"]
			size = listed["size"]
			digest_md5 = listed["md5"]
			digest_sha256 = listed["sha256"]
			
			key = "{0}:{1}:{2}".format(size, digest_md5, digest_sha256)
			
			collected_files[key].append(path)
		
		similar_files = (listed for _, listed in collected_files.iteritems() if len(listed) > 1)
		
		for listed in similar_files:
			self.create_symlinks(listed)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create hardlinks for similar files in directory.')
	parser.add_argument("-s", "--min-size", type=int, default="1024", help='minimal file size to check (bytes)')
	parser.add_argument('files', metavar='file', type=str, nargs='+', help='list of files or directories')

	args = parser.parse_args()
	
	deduplicator = Deduplicator(args.files, args.min_size)
	deduplicator.process()
