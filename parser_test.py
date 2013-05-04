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

	def test_at_repliee(self):
		instruction = Instruction("tannerld: @ryan Things are crazy here.")

		self.assertEqual(instruction.status, "@ryan Things are crazy here.")
		self.assertEqual(instruction.at_repliee, "ryan")

		instruction = Instruction("tannerld: Things are crazy here.")

		self.assertEqual(instruction.status, "Things are crazy here.")
		self.assertEqual(instruction.at_repliee, None)

		instruction = Instruction("tannerld: Things are crazy here at the @ryan house.")

		self.assertEqual(instruction.status, "Things are crazy here at the @ryan house.")
		self.assertEqual(instruction.at_repliee, None)

	def test_mentions(self):
		self.assertEqual(Instruction("tannerld: @ryan Things are crazy here.").mentions, [])
		self.assertEqual(Instruction("tannerld: Things are crazy here.").mentions, [])
		self.assertEqual(Instruction("tannerld: I love @ryan's house.").mentions, ["ryan"])
		self.assertEqual(Instruction("tannerld: I love the @ryan house.").mentions, ["ryan"])
		self.assertEqual(Instruction("tannerld: This cat is awesome. @ryan").mentions, ["ryan"])
		self.assertEqual(Instruction("tannerld: Having dinner with @ryan and @bob.").mentions, ["ryan", "bob"])

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

	def test_is_retweet(self):
		self.assertTrue(Instruction("ryan: RT @tannerld Is this life?").is_retweet())
		self.assertFalse(Instruction("tannerld: Is this life! No.").is_retweet())
		self.assertFalse(Instruction("tannerld: @ryan Things are crazy here.").is_retweet())

	def test_retweet(self):
		self.assertEqual(Instruction("ryan: RT @tannerld Is this life?").retweet(), ("tannerld", "Is this life?"))
		self.assertEqual(Instruction("tannerld: Is this life! No.").retweet(), (None, None))
		self.assertEqual(Instruction("tannerld: @ryan Things are crazy here.").retweet(), (None, None))

class TestParser(unittest.TestCase):
	def setUp(self):
		self.output = StringIO.StringIO()
		self.input = StringIO.StringIO()

	def tearDown(self):
		self.output.close()
		self.input.close()

	def test_hello_world(self):
		parser = Parser.from_file("hello_world.twttr")
		parser.output = self.output
		parser.input = self.input

		parser.run()

		self.assertEqual(self.output.getvalue(), "Hello World!")

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

	def test_at_reply(self):
		code = """tannerld: I am the one.
ryan: I am not the one.
tannerld: @ryan Are you sure?"""

		parser = Parser(code)

		parser.run()

		self.assertEqual(parser.variables['tannerld'], 8)
		self.assertEqual(parser.variables['ryan'], 5)

	def test_mentions(self):
		code = """tannerld: This is not cool.
ryan: I love driving in cars.
tannerld: I'm not sure I like @ryan's car."""

		parser = Parser(code)

		parser.run()

		self.assertEqual(parser.variables['tannerld'], 6)
		self.assertEqual(parser.variables['ryan'], 5)

	def test_input(self):
		code = """tannerld: Do you know the answer?
ryan: I do not know. But do you know?"""

		parser = Parser(code)
		parser.output = self.output
		parser.input = self.input

		self.input.write('aa')
		self.input.seek(0)

		parser.run()

		self.assertEqual(parser.variables['tannerld'], 102)
		self.assertEqual(parser.variables['ryan'], 97)

	def test_printing(self):
		code = """tannerld: It was a triumph!
ryan: My best was then. My worst will be tomorrow!"""

		parser = Parser(code)
		parser.output = self.output
		parser.input = self.input

		parser.run()

		self.assertEqual(self.output.getvalue(), chr(4))

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