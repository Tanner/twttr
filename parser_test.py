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

	def test_extract_hashtags(self):
		instruction = Instruction("tannerld: I love #cats. Maybe. #kitty")

		self.assertEqual(instruction.hashtags, ["cats", "kitty"])

		instruction = Instruction("tannerld: I love cats.")

		self.assertEqual(instruction.hashtags, [])

	def test_value(self):
		self.assertEqual(Instruction("tannerld: I love cats. Maybe.").value(), 2)
		self.assertEqual(Instruction("tannerld: I love cats.").value(), 3)
		self.assertEqual(Instruction("tannerld: Hmm. That darn cat.").value(), -2)
		self.assertEqual(Instruction("tannerld: I love you. That darn cat.").value(), 0)
		self.assertEqual(Instruction("tannerld: Is this right... No.").value(), 2)
		self.assertEqual(Instruction("tannerld: I'm not sure. This is mine.").value(), 0)

	def test_input(self):
		self.assertTrue(Instruction("tannerld: Is this life?").is_input())
		self.assertFalse(Instruction("tannerld: Is this life? No.").is_input())

	def test_output(self):
		self.assertTrue(Instruction("tannerld: Is this life!").is_output())
		self.assertFalse(Instruction("tannerld: Is this life! No.").is_output())

if __name__ == '__main__':
	unittest.main()