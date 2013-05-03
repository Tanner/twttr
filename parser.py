#! /usr/bin/env python

from __future__ import print_function

import re
import sys
import warnings

class Instruction:
	"""Class that represents a twttr instruction."""

	def __init__(self, instruction):
		"""Create an instruction given its string."""
		match = re.match(r"([a-zA-Z]+): (.+)", instruction)

		if match == None:
			raise ValueError('Instruction is not valid format of "author: status"')

		self.author = match.group(1)
		self.status = match.group(2)

		if len(self.status) > 140:
			raise ValueError('Tweet must be less than or equal to 140 characters')

		self.status_no_hashtags = self.__remove_hashtags()
		self.hashtags = self.__extract_hashtags()

	def value(self):
		"""Read the value of the status based on the number of words in the first two sentences."""
		fragments = re.findall(r"([A-Za-z '-]+)[\.,!;\?:-] ?", self.status)

		if len(fragments) == 1:
			return self.__count_words(fragments[0])

		return self.__count_words(fragments[0]) - self.__count_words(fragments[1])

	def is_input(self):
		"""Detect whether the instruction is asking for input."""
		return self.status_no_hashtags[-1] == '?'

	def is_output(self):
		"""Detect whether the instruction is a print."""
		return self.status_no_hashtags[-1] == '!'

	def __count_words(self, string):
		"""Count the number of words in a string."""
		return len(re.findall(r"([A-Za-z\.\"-']+) ?", string))

	def __extract_hashtags(self):
		"""Extract the hashtags (#tag) from the status."""
		return re.findall(r"#([A-Za-z]+)", self.status)

	def __remove_hashtags(self):
		"""Return the status of any hashtags."""
		return re.sub(r"#[A-Za-z]+", "", self.status).strip()

class Parser:
	"""Class that parses a twttr program."""

	def __init__(self, code):
		"""Create a parser using the given twttr program."""
		self.instructions = []
		self.variables = {}

		self.input = sys.stdin
		self.output = sys.stdout

		lines = code.splitlines()

		for line in lines:
			self.instructions.append(Instruction(line))

		self.hashtags = {}

		# Extract hashtags from all the instructions for branching purposes
		for i in reversed(range(len(self.instructions))):
			instruction = self.instructions[i]

			for hashtag in instruction.hashtags:
				if hashtag in self.hashtags:
					self.hashtags[hashtag].append(i)
				else:
					self.hashtags[hashtag] = [i]

	@classmethod
	def from_file(self, file):
		"""Read in code from a file and create a parser."""
		with open(file, 'r') as f:
			return self(f.read())

	def run(self, debug=False):
		"""Run the twttr program."""
		looping = False

		pc = len(self.instructions) - 1
		while pc >= 0:
			instruction = self.instructions[pc]

			if instruction.author not in self.variables:
				self.variables[instruction.author] = 0

			self.variables[instruction.author] += instruction.value()

			if instruction.is_input():
				self.output.write(instruction.status + " ")
				input = self.input.read(1)

				if len(input) > 0:
					self.variables[instruction.author] += ord(input[0])
			elif instruction.is_output():
				if self.variables[instruction.author] in range(256):
					if debug:
						self.output.write("%s\n" % chr(self.variables[instruction.author]))
					else:
						self.output.write("%s" % chr(self.variables[instruction.author]))

			if debug:
				self.output.write("PC = %d %s\n", pc, self.variables)

			hashtags = instruction.hashtags

			if len(hashtags) > 0:
				for hashtag in hashtags:
					if len(self.hashtags[hashtag]) > 0:
						# Found a hashtag that has more than one instance
						indices = self.hashtags[hashtag]

						current_index = indices.index(pc)

						if current_index == len(indices) - 1:
							# Currently at the last instance of this hashtag
							if self.variables[instruction.author] != 0:
								pc = indices[0]
								looping = True
							else:
								looping = False
						else:
							# Not at the last instance of this hashtag
							if looping:
								pc = indices[current_index + 1]

						break

			if not looping:
				pc -= 1

def main():
	"""Run that twttr program taking the first CLI argument to be the file containing the program."""
	parser = Parser.from_file(sys.argv[1])

	parser.run()

if __name__ =='__main__':
	main()