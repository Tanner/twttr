#! /usr/bin/env python

import re
import sys
import warnings

class Instruction:
	"""Class that represents a twttr instruction."""

	def __init__(self, instruction):
		match = re.match(r"([a-zA-Z]+): (.+)", instruction)

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

	def remove_hashtags(self):
		"""Return the status of any hashtags."""
		return re.sub(r"#[A-Za-z]+", "", self.status).strip()

	def value(self):
		"""Read the value of the status based on the number of words in the first two sentences."""
		fragments = re.findall(r"([A-Za-z '-]+)[\.,!;\?:-] ?", self.status)

		if len(fragments) == 1:
			return self.__count_words(fragments[0])

		return self.__count_words(fragments[0]) - self.__count_words(fragments[1])

	def is_input(self):
		"""Detects whether the instruction is asking for input."""
		return self.remove_hashtags()[-1] == '?'

	def is_output(self):
		"""Detects whether the instruction is a print."""
		return self.remove_hashtags()[-1] == '!'

	def __count_words(self, string):
		"""Count the number of words in a string."""
		return len(re.findall(r"([A-Za-z\.\"-']+) ?", string))

class Parser:
	"""Class that parses a twttr program."""

	def __init__(self, file):
		self.instructions = []
		self.variables = {}

		with open(file, 'r') as f:
			for line in f:
				self.instructions.append(Instruction(line))

		self.hashtags = {}

		for i in reversed(range(len(self.instructions))):
			instruction = self.instructions[i]

			for hashtag in instruction.extract_hashtags():
				if hashtag in self.hashtags:
					self.hashtags[hashtag].append(i)
				else:
					self.hashtags[hashtag] = [i]

	def run(self):
		for i in reversed(range(len(self.instructions))):
			instruction = self.instructions[i]

			if instruction.author not in self.variables:
				self.variables[instruction.author] = 0
			
			if instruction.is_input():
				input = raw_input(instruction.status + " ")

				if len(input) > 0:
					self.variables[instruction.author] += ord(input[0])
			elif instruction.is_output():
				print chr(self.variables[instruction.author])

			self.variables[instruction.author] += instruction.value()

		print self.variables

def main():
	parser = Parser(sys.argv[1])

	parser.run()

if __name__ =='__main__':
	main()