#! /usr/bin/env python

import StringIO
import sys
import unittest

from parser import Instruction, Parser

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

class TestParser(unittest.TestCase):
	def setUp(self):
		sys.stdout = self.output = StringIO.StringIO()

	def tearDown(self):
		self.output.close()

		sys.stdout = sys.__stdout__

	def test_hello_world(self):
		parser = Parser.from_file("hello_world.twttr")

		parser.run()

		self.assertEqual(self.output.getvalue(), "Hello World!\n")

	def test_basic_math(self):
		code = """tannerld: My cat.
ryan: This is my life. I think so.
carly: No. I don't like you.
fred: I think this is my life!
bob: I hate all of you. Again I hate all of you!"""

		parser = Parser(code)

		parser.run()

		self.assertEqual(parser.variables['tannerld'], 2)
		self.assertEqual(parser.variables['ryan'], 1)
		self.assertEqual(parser.variables['carly'], -3)
		self.assertEqual(parser.variables['fred'], 6)
		self.assertEqual(parser.variables['bob'], -1)

	def test_printing(self):
		code = """tannerld: It was a triumph!
ryan: My best was then. My worst will be tomorrow!"""

		parser = Parser(code)

		parser.run()

		self.assertEqual(self.output.getvalue(), chr(4) + "\n")

	def test_branching(self):
		code = """tannerld: My cat hates me. It knows something about me. #cat
ryan: Plus two. Maybe. #cat
tannerld: I love my kitty cat."""

		parser = Parser(code)

		parser.run()

		self.assertEqual(parser.variables['tannerld'], 0)
		self.assertEqual(parser.variables['ryan'], 5)

if __name__ == '__main__':
	unittest.main()