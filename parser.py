#! /usr/bin/env python

import re
import sys
import warnings

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

	def is_creation(self):
		"""Detects whether the instruction is a variable declaration."""
		return re.search(r"first [tweet|status|post]", self.status, re.IGNORECASE) != None

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

class Parser:
	"""Class that parses a twttr program."""

	def __init__(self, file):
		self.instructions = []
		self.variables = {}

		with open(file, 'r') as f:
			for line in f:
				self.instructions.append(Instruction(line))

	def run(self):
		for i in reversed(range(len(self.instructions))):
			instruction = self.instructions[i]

			if instruction.is_creation():
				if instruction.author not in self.variables:
					self.variables[instruction.author] = 0
				else:
					warnings.warn("Warning: Reached variable creation tweet, but user already a variable", RuntimeWarning)
			elif instruction.is_input():
				input = raw_input(instruction.status + " ")

				if len(input) > 0:
					self.variables[instruction.author] += ord(input[0])
			elif instruction.is_output():
				print chr(self.variables[instruction.author])
			else:
				self.variables[instruction.author] += instruction.value()

def main():
	parser = Parser(sys.argv[1])

	parser.run()

if __name__ =='__main__':
	main()