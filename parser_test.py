#! /usr/bin/env python

import unittest

from parser import Instruction

class TestInstruction(unittest.TestCase):
	def test_construction(self):
		with self.assertRaises(ValueError):
			instruction = Instruction("Random string of characters that is not the right format")

		with self.assertRaises(ValueError):
			instruction = Instruction("tannerld: A very long tweet that is much longer than 140 characters I think I will run out of breath. Maybe we should go out to dinner later, but I'm not really sure.")

		instruction = Instruction("tannerld: I love cats. Maybe.")
		self.assertEqual(instruction.author, "tannerld")
		self.assertEqual(instruction.status, "I love cats. Maybe.")

if __name__ == '__main__':
	unittest.main()