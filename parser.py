#! /usr/bin/env python

import re

class Instruction:
	"""Class that represents a twttr instruction."""

	def __init__(self, instruction):
		match = re.match(r"([a-zA-Z]+): (.*)", instruction)

		if match == None:
			raise ValueError('Instruction is not valid format of "author: status"')

		self.author = match.group(1)
		self.status = match.group(2)

		if len(self.status) > 140:
			raise ValueError('Tweet must be less than or equal to 140 characters')

		self.hashtags = self.extract_hashtags();

	def extract_hashtags(self):
		"""Extracts the hashtags (#tag) from the status."""
		return re.findall(r"#([A-Za-z]+)", self.status)