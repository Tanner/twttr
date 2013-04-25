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

	def value(self):
		"""Read the value of the status based on the number of words in the first two sentences."""
		fragments = re.findall(r"([A-Za-z ]+)[\.,;:-] ?", self.status)

		if len(fragments) == 1:
			return self.__count_words(fragments[0])

		return self.__count_words(fragments[0]) - self.__count_words(fragments[1])

	def is_input(self):
		"""Detects whether the instruction is asking for input."""
		return self.status[-1] == '?'

	def is_output(self):
		"""Detects whether the instruction is a print."""
		return self.status[-1] == '!'

	def __count_words(self, string):
		"""Count the number of words in a string."""
		return len(re.findall(r"([A-Za-z\.\"-]+) ?", string))